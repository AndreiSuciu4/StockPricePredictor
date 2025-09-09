import {Component, OnInit} from '@angular/core';
import {Company} from "../../common/company";
import {StockMarketService} from "../../service/stock-market.service";
import {HttpErrorResponse} from "@angular/common/http";
import {Router} from "@angular/router";
import {GeneratedPrediction} from "../../common/generatedPrediction";
import {lastValueFrom} from "rxjs";


@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent implements OnInit{
    companies: Company[];
    selectedCompany: Company;
    generatedValue: number;
    load:boolean = false;
    dropdownVisible = false;
    fullName!: string;
    showNotification: boolean = false;
    generatedPredictions!: GeneratedPrediction[];

  constructor(private stockService: StockMarketService,
              private router: Router) {
      this.generatedValue = -1;
      this.companies = [
        {name: 'Apple', code: 'AAPL'},
        {name: 'Google', code: 'GOOG'},
        {name: 'Microsoft', code: 'MSFT'},
        {name: 'Amazon', code: 'AMZN'}
      ];
      this.selectedCompany = {name: 'Apple', code: 'AAPL'};
      this.fullName = sessionStorage.getItem("firstname") + " " +  sessionStorage.getItem("lastname");
  }

  ngOnInit() {
    let predictions = sessionStorage.getItem('generatedPredictions');

    if (predictions != null) {
      this.generatedPredictions = JSON.parse(sessionStorage.getItem('generatedPredictions') || '[]');
      this.showNotification = true;
      sessionStorage.removeItem('generatedPredictions');
    }
  }
  generateValue() {
      this.load = true;
      let stock = this.selectedCompany.code;
      lastValueFrom(this.stockService.getPredictedValue(stock))
        .then((response: any) => {
          if (response) {
            let prediction = response.prediction

            this.generatedValue = prediction.toFixed(3);
            this.load = false;
          }
        })
        .catch((error: HttpErrorResponse) => {
          if (error.status === 401)
            this.router.navigate(["login"]);
          this.load = false;
        })
  }

  companyChanged() {
      this.generatedValue = -1;
  }
  toggleDropdown() {
    this.dropdownVisible = !this.dropdownVisible;
  }

  logout() {
    sessionStorage.clear();
    this.router.navigate(["login"]);
  }

  protected readonly parseFloat = parseFloat;
}

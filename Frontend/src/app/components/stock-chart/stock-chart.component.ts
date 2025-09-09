import {Component, Input, OnChanges, ViewEncapsulation} from '@angular/core';
import {StockMarketService} from "../../service/stock-market.service";
import {Router} from "@angular/router";
import {HttpErrorResponse} from "@angular/common/http";
import {lastValueFrom} from "rxjs";

@Component({
  selector: 'app-stock-chart',
  template:
    `<div class="chart">
      <ejs-stockchart id="chart-container" [primaryXAxis]='primaryXAxis'[primaryYAxis]='primaryYAxis' [title]='title' [crosshair]='crosshair' >
        <e-stockchart-series-collection>
            <e-stockchart-series [dataSource]='chartData' type='Candle' xName='date' yName='open' name='India' width=2 ></e-stockchart-series>
        </e-stockchart-series-collection>
      </ejs-stockchart>
    </div>
    <ngx-loading [show]="load"></ngx-loading>
    `,
  styleUrls: ['./stock-chart.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class StockChartComponent implements OnChanges {
  @Input() stock: string;
  public primaryXAxis: Object;
  public primaryYAxis: Object;
  public chartData: Object[];
  public title: string;
  public crosshair: Object;
  load: boolean = true;

  constructor(private stockService: StockMarketService,
              private router: Router)  {
    this.stock = 'AAPL';

    this.loadData();
    this.chartData = []
    this.title = 'History price for ' + this.stock;
    this.primaryXAxis = {
      valueType: 'DateTime',
      crosshairTooltip: {enable:true}
    };
    this.primaryYAxis = {
      majorTickLines: { color: 'transparent', width: 0 },
      crosshairTooltip: {enable:true}
    };
    this.crosshair= {
      enable: true
    };
  }

  ngOnChanges() {
    this.load = true;
    this.loadData();
    this.title = 'History price for ' + this.stock;
  }

  private loadData() {
    lastValueFrom(this.stockService.getHistoryData(this.stock))
      .then((response:any) =>{
        let historyData: any = [];
        if (response) {
          let history_data = response.history_data;

          history_data = JSON.parse(history_data);
          for (const stock_data of history_data) {
            historyData.push({
              date: stock_data.trading_date,
              open: stock_data.open_price.toString(),
              close: stock_data.close_price.toString(),
              high: stock_data.high_price.toString(),
              low: stock_data.low_price.toString()
            })
          }
          this.chartData = historyData;
          this.load = false;
        }
      })
      .catch((error: HttpErrorResponse) =>{
        if(error.status === 401)
            this.router.navigate(["login"]);
      });
  }
}


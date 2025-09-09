import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import {
  ChartModule,
  RangeNavigatorModule,
  StockChartAllModule,
  ChartAllModule,
  CategoryService, LineSeriesService
} from '@syncfusion/ej2-angular-charts';
import { HttpClientModule} from "@angular/common/http";
import { HomePageComponent } from './components/home-page/home-page.component';
import { StockChartComponent } from './components/stock-chart/stock-chart.component';
import {DropdownModule} from "primeng/dropdown";
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import {ButtonModule} from "primeng/button";
import { NgxLoadingModule, NgxLoadingConfig } from "ngx-loading";
import { LoginPageComponent } from './components/login-page/login-page.component';
import { RegisterPageComponent } from './components/register-page/register-page.component';
import {CardModule} from "primeng/card";
import {AppComponent} from "./app.component";
import {InputTextModule} from "primeng/inputtext";
import {MessageModule} from "primeng/message";

const ngxLoadingXConfig: NgxLoadingConfig = {
  fullScreenBackdrop: true
}

@NgModule({
  declarations: [
    HomePageComponent,
    StockChartComponent,
    RegisterPageComponent,
    LoginPageComponent,
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    DropdownModule,
    FormsModule,
    ReactiveFormsModule,
    MatSelectModule,
    ChartModule,
    RangeNavigatorModule,
    StockChartAllModule,
    ChartAllModule,
    ButtonModule,
    NgxLoadingModule.forRoot(ngxLoadingXConfig),
    CardModule,
    InputTextModule,
    MessageModule,
  ],
  bootstrap: [AppComponent],
  providers: [ CategoryService, LineSeriesService ]
})
export class AppModule { }

import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {baseUrl, generatePredictionPath, historyDataPath} from "../Constants";

@Injectable({
  providedIn: 'root'
})
export class StockMarketService {

  constructor(private http: HttpClient) { }

  getHistoryData(stock: string) {
    const token = sessionStorage.getItem("token");
    const headers = new HttpHeaders().set('x-access-token', token || '');

    let url = baseUrl + historyDataPath + "?stock=" + stock;

    return this.http.get(url, { headers });
  }

  getPredictedValue(stock: string) {
    const token = sessionStorage.getItem("token");
    const headers = new HttpHeaders().set('x-access-token', token || '');

    let url = baseUrl + generatePredictionPath + "?stock=" + stock;

    return this.http.get(url, { headers });
  }
}

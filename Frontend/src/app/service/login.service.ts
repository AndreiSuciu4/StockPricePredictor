import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import jwt_decode from 'jwt-decode'
import {baseUrl, loginPath} from "../Constants";

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  constructor(private httpClient: HttpClient) { }

  public authenticate(credentials: any) {
    let url = baseUrl + loginPath
    return this.httpClient.post<any>(url, JSON.stringify(credentials), {
      headers: {'Content-type': "application/json"},
      observe: 'response'
    });
  }

  public getDecodedToken(token: string): any {
    try{
      return jwt_decode(token)
    } catch (Error) {
      return  null;
    }
  }
}

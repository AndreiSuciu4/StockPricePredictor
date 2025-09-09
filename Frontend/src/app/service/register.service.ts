import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {User} from "../common/user";
import jwt_decode from "jwt-decode";
import {baseUrl, registerPath} from "../Constants";

@Injectable({
  providedIn: 'root'
})
export class RegisterService {

  constructor(private httpClient: HttpClient) { }

  public registerUser(user: User) {
    let url = baseUrl + registerPath
    return this.httpClient.post<any>(url, user, {
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

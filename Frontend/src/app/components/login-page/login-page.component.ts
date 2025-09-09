import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import {LoginService} from "../../service/login.service";
import {lastValueFrom} from "rxjs";
import {HttpErrorResponse} from "@angular/common/http";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css']
})
export class LoginPageComponent implements OnInit {
  loginForm!: FormGroup;
  error: boolean = false;
  load: boolean = false;
  constructor(private formBuilder: FormBuilder,
              private loginService: LoginService,
              private router: Router) { }

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  onLogin() {
    if (this.loginForm.valid) {
      this.load = true;
      const response = this.loginService.authenticate(this.loginForm.value)
      lastValueFrom(response)
        .then(response => {
            if(response) {
              let generated_predictions = response.body.generated_predictions
              if (generated_predictions != "[]")
                sessionStorage.setItem('generatedPredictions', generated_predictions);

              let token = response.body.token;
              let decodedToken = this.loginService.getDecodedToken(token);
              sessionStorage.setItem("firstname", decodedToken["firstname"])
              sessionStorage.setItem("lastname", decodedToken["lastname"])
              sessionStorage.setItem("token", token);
              this.load = false;
              this.error = false;

              this.router.navigate(['home-page']);            }
          },
          (_: HttpErrorResponse) => {
            this.error = true;
            this.load = false;
          }
        )
    }
  }

  onRegister() {
    this.router.navigate(["register"]);
  }
}

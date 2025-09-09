import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {RegisterService} from "../../service/register.service";
import {lastValueFrom} from "rxjs";
import {HttpErrorResponse} from "@angular/common/http";
import {Router} from "@angular/router";

@Component({
  selector: 'app-register-page',
  templateUrl: './register-page.component.html',
  styleUrls: ['./register-page.component.css']
})
export class RegisterPageComponent implements OnInit{
  registerForm!: FormGroup;
  error: boolean = false;
  load: boolean = false;

  constructor(private formBuilder: FormBuilder,
              private registerService: RegisterService,
              private router: Router) { }

  ngOnInit() {
    this.registerForm = this.formBuilder.group({
      'firstName': ['', Validators.required],
      'lastName': ['', Validators.required],
      'email': ['', [Validators.required, Validators.email]],
      'password': ['', [Validators.required, Validators.minLength(3)]]
    });
  }

  onRegister() {
    if (this.registerForm.valid) {
      this.load = true;
      const response = this.registerService.registerUser(this.registerForm.value)
      lastValueFrom(response)
        .then(response => {
            if (response) {
              let token = response.body.token;
              let decodedToken = this.registerService.getDecodedToken(token);

              sessionStorage.setItem("firstname", decodedToken["firstname"])
              sessionStorage.setItem("lastname", decodedToken["lastname"])
              sessionStorage.setItem("token", token);

              this.load = false;
              this.error = false;
              this.router.navigate(["home-page"]);
            }
          },
          (_: HttpErrorResponse) => {
            this.error = true;
            this.load = false;
          }
        )
    }
  }
}

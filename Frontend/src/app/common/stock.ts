export class Stock {
  public Date: string;
  public Open: number;
  public High: number;
  public Low: number;
  public Close: number;
  public AdjClose: number;
  public Volume: number;


  constructor(Date: string, Open: number, High: number, Low: number, Close: number, AdjClose: number, Volume: number) {
    this.Date = Date;
    this.Open = Open;
    this.High = High;
    this.Low = Low;
    this.Close = Close;
    this.AdjClose = AdjClose;
    this.Volume = Volume;
  }
}

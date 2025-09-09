class TradingIndicator:
    @staticmethod
    def get_williams_indicator(data_frame):

        high = data_frame['High']
        low = data_frame['Low']
        close = data_frame['Close']

        highest_high = max(high)
        lowest_low = min(low)
        current_close = close[len(close) - 1]

        wpr = (highest_high - current_close) / (highest_high - lowest_low) * -100

        return wpr

    @staticmethod
    def get_relative_strength_index(data_frame):

        close = data_frame['Close']

        gain = 0
        loss = 0

        for j in range(1, len(close)):
            diff = close[j] - close[j - 1]
            if diff >= 0:
                gain += diff
            else:
                loss += abs(diff)

        avg_gain = gain / 14
        avg_loss = loss / 14

        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        return rsi

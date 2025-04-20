

class Broker:
    stock_prices={'goog':400,'amzn':900,'tsla':200}
     
    def __init__(self,name,acc_no,money):
          self.name=name
          self.acc_no=acc_no
          self.wallet=money
          self.portfolio={}
    
    def get_portfolio(self):
        if self.portfolio!={}:
            for i,j in self.portfolio.items():
                  print(i,j)
            print('-----------------')
        else:
             print('empty')
    def buy(self,stock_name):
        found=self.stock_prices.get(stock_name)
        if found:
            if self.wallet>found:
                self.portfolio.update({stock_name:found})
                self.wallet=self.wallet-found
                print(f'bought {stock_name} at price {found}')
            else:
                 print('not enough money')
        else:
             print('stock not found')
        
    
    def sell(self,stock_name):
        found=self.portfolio.get(stock_name)
        if found:
              self.portfolio.pop(stock_name)
              self.wallet=self.wallet+found
              print(f'sold {stock_name} at price {found}')
        else:
             print('stock not found')


a=100

def get_number():
     return 200

if __name__=="__main__":
    print('this is file 1')
import cv2
import easyocr



def ocro(image1):
    image = cv2.imread(image1)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    reader = easyocr.Reader(['en'])
    results = reader.readtext(gray)

    amount = None
    cars = []
    i=0
    for result in results:
        cars.append(result[1])
        
        
    l= len(cars)
    for i in range(0,l):
        text = cars[i]
        if(i < l-1):
            if 'ROUNDED TOTAL' in text or 'Total' in text:
                if '-' in cars[i+1]: 
                    amount=cars[i+1].replace('-', '.')  
                    break
                elif(cars[i+1].isdigit()):
                    amount=cars[i+1]  
                    break

    if amount:
        if '-' in amount: 
            amount=amount.replace('-', '.')  
            return amount
        else:
            return amount
    else:
        print('Failed to extract the amount')
        
        
    
    

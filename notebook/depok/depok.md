
# Making Better Decision (with Data Science) on Buying a House
## Behind the Notebook Story

* Everybody wants the best house to buy but not everyone has a lot of money.

* For those people who felt that money is a scarce resource, this Jupyter Notebook illustrates how data analysis might help you in making the important decision

## Python Solution for Your Better Decision Making
### Importing Python Packages


```python
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
```


```python
%matplotlib inline
plt.style.available
plt.style.use('seaborn-poster')
pd.set_option('display.max_colwidth', -1)
```

### Defining Python Functions

#### Define Unit of Measures


```python
def unitMeasures():
    
    unit={}
    
    unit['price'] = "million IDR"
    unit['land'] = 'square meters'
    unit['building'] = 'square meters'
    
    return unit
```


```python
unit = unitMeasures()
unit
```




    {'building': 'square meters', 'land': 'square meters', 'price': 'million IDR'}



#### Visualizing Data, Seeing is Believing


```python
def visualizeData(AREA, minPRICE, maxPRICE):
    
    filename = 'OUTPUT/'+AREA+'-between-'+str(minPRICE)+'-'+str(maxPRICE)+'.csv'
    chartTitle = 'House for Sale in '+AREA.title()+'\nbetween '+str(minPRICE)+' - '+str(maxPRICE) + ' (' + unit['price'] + ')\n'+'\n\n'
    names = ['price','land','building','bed','bath','url']
     
    try:
        df = pd.read_csv(filepath_or_buffer = filename, header=0, names=names)
        df = df.drop_duplicates()
        df = df.replace(r'None', np.nan, regex=True)
        df = df.dropna()

        df = df.sort_values(['price'])
        
        chart1 = df[(['price','land','building'])].astype(float).plot(x='price', y=['land','building'], title = chartTitle);
        lines, labels = chart1.get_legend_handles_labels();
        en_labels = [r'land $(m^{2})$',r'building $(m^{2})$']
        chart1.legend(lines, en_labels, loc='best');
        chart1.set_xlabel('\nPrice (million IDR)');
       
        return df
        
    except IOError:
    
        print "file '"+filename+ "' not found!\n\nplease run the following command:\n'python getHouseforSale.py " +AREA+' '+str(minPRICE)+' '+str(maxPRICE) +"'"
    
```

#### Finding Most Spacious House


```python
def mostSpacious(df):

    maxland = df.ix[df[(['price','land'])].astype(int).sort_values('land').idxmax()['land']]
    print "\nMOST SPACIOUS LAND\n-----------------\n"
    for item in sorted(maxland.iteritems()):
        print '{:>8}  {:>4}'.format(item[0], item[1])
        
    maxbuilding = df.ix[df[(['price','building'])].astype(int).sort_values('building').idxmax()['building']]

    print "\nMOST SPACIOUS BUILDING\n-----------------\n"
    for item in sorted(maxbuilding.iteritems()):
        print '{:>8}  {:>4}'.format(item[0], item[1])
```

#### Finding Average Measures


```python
def averageMeasures(df):
    avg = {}
    print "\nAVERAGE MEASURES\n-----------------\n"    
    avg['price'] = np.ceil(df['price'].astype(int).mean())
    avg['land'] = np.ceil(df['land'].astype(int).mean())
    avg['building'] = np.ceil(df['building'].astype(int).mean())
    #avg['bed'] = np.ceil(df['bed'].astype(int).mean())
    #avg['bath'] = np.ceil(df['bath'].astype(int).mean())
    
    for k, v in sorted(avg.iteritems()):
        print '{:>8}  {:>4}'.format(k, int(v))
    
    return avg
```

#### Finding Economical House


```python
def selectEconomical(df, avg, unit):
  
    df1 = df[(df['price'] < avg['price'])]
    
    if not df1.empty:

        df2 = df1[(df1['land'].astype(int) > avg['land'])]
        
        if df2.empty:
            
            print "\nECONOMICAL\n-----------------\n"
            print "\nAmong which there are:", df1.count()['price'], " items with still below average price: "+str(int(avg['price']))+" ("+unit['price']+")"+"."

        else:
            
            df3 = df2[(df2['building'].astype(int) > avg['building'])]
            
            if df3.empty:
           
                print "\nAmong which there are:", df2.count()['land'], " items with land above average: "+str(int(avg['land']))+" ("+unit['land']+")"+"."
                print df2[(['price','land','building','url'])].sort_values(['price','land','building'], ascending=[1,0,0]).to_string(index=False)
            
            else:
                
                print "\nMOST ECONOMICAL\n-----------------\nis when the price is really below average: "+str(int(avg['price']))+" ("+unit['price']+")"+" but you get above the average land: "+str(int(avg['land']))+" ("+unit['land']+")"+" and above the average building: "+str(int(avg['building']))+" ("+unit['land']+")"+"\n"
                print "You are blessed to choose one of these", df3.count()['building'], " houses:\n"            
                print df3[(['price','land','building','url'])].sort_values(['price','land','building'], ascending=[1,0,0]).to_string(index=False)
                #print df3[(['price','land','building'])].astype(int).sort_values(['price','land','building'],ascending=[1,0,0])
 
    else:
        
        print "I am sorry, but there is no economical category within this price range..."
```

#### FInd Moderate Price House


```python
def selectModerate(df, avg, unit):
       
    # MODERATE and EXPENSIVE when the price equals or greater than average price
    # MODERATE when you got average or better land/building
    # EXPENSIVE when you got below average land/ building

    df1 = df[(df['price'] >= avg['price'])]
    
    if df1.empty:
        
        print "\nLESS ECONOMICAL\n-----------------\nThere are:", df1.count()['price'], " items above-average price."      

    else:
        
        print "\nMODERATE PRICE\n-----------------\nis when the price is above average: "+str(int(avg['price']))+" ("+unit['price']+")"+" with above-average land: "+str(int(avg['land']))+" ("+unit['land']+")"+" and above-average building: "+str(int(avg['building']))+" ("+unit['building']+")"+"\n"
        df2 = df1[(df1['land'].astype(int) >= avg['land'])]
        print "\nThere are :", df2.count()['land'], " items with above-average price and above-average land."
        
        if not df2.empty:
            
            df3 = df2[(df2['building'].astype(int) >= avg['building'])]
            print "\nThere are :", df3.count()['building'], " items with above-average price, above-average land and above-average building.\n"
            print df3[(['price','land','building','url'])].sort_values(['price','land','building'], ascending=[1,0,0]).to_string(index=False)

```

#### Find Expensive House


```python
def selectExpensive(df, avg, unit):
       
    # MODERATE and EXPENSIVE when the price equals or greater than average price
    # MODERATE when you got average or better land/building
    # EXPENSIVE when you got below average land/ building

    df1 = df[(df['price'] >= avg['price'])]
    
    print "\nEXPENSIVE PRICE\n-----------------\nis when the price is above average: "+str(int(avg['price']))+" ("+unit['price']+")"+" but you only get land below average: "+str(int(avg['land']))+" ("+unit['land']+")"+" and building below average: "+str(int(avg['building']))+" ("+unit['building']+").\n\n"
    
    if not df1.empty:

        df2 = df1[(df1['land'].astype(int) < avg['land'])]
        
        if not df2.empty:
            
            df3 = df2[(df2['building'].astype(int) < avg['building'])]
            print "\nThere are :", df3.count()['building'], " items that matched the EXPENSIVE category.\n"

            print df3[(['price','land','building','url'])].sort_values(['price','land','building'], ascending=[1,0,0]).to_string(index=False)
            
```

## Application
### House Price Between 100 - 200 Mio IDR

#### Visualize Data


```python
df = visualizeData('depok', 100, 200);
```


![png](png/output_22_0.png)


### Analyze the Data of House Prices Between 100 - 200 Mio IDR

#### Calculate Average Measures


```python
avg = averageMeasures(df)
```

    
    AVERAGE MEASURES
    -----------------
    
    building    40
        land    55
       price   159
    


```python
mostSpacious(df)
```

    
    MOST SPACIOUS LAND
    -----------------

        bath     1
         bed     2
    building    63
        land   160
       price   185
         url   http://rumahdijual.com/depok/957749-rumah-lt-160-lb-63-di-cilangkap-depok-sebelum.html
    
    MOST SPACIOUS BUILDING
    -----------------
    
        bath     2
         bed     2
    building   115
        land   135
       price   200
         url   http://rumahdijual.com/depok/968717-rumah-lt-135-lb-115-di-kp-setu-cilangkap.html
    


```python
selectEconomical(df, avg, unit)
```

    
    MOST ECONOMICAL
    -----------------
    is when the price is really below average: 159 (million IDR) but you get above the average land: 55 (square meters) and above the average building: 40 (square meters)
    
    You are blessed to choose one of these 27  houses:
    
    price  land  building                                                                                                     url
    100    72    55         http://rumahdijual.com/depok/1222395-rumah-take-over-di-depok.html                                   
    110    72    45         http://rumahdijual.com/depok/1033605-rumah-bagus-di-cilodong-depok-view-setu-cilodong.html           
    115    60    50         http://rumahdijual.com/depok/862918-hunian-terlaris-dekat-stasiun-citayam-minimalist.html            
    120    76    56         http://rumahdijual.com/depok/1142658-rumah-oper-kredit.html                                          
    123    105   68         http://rumahdijual.com/depok/1178236-rumah-minimalis-mewah-murah-di-depok-permata-cimanggis.html     
    123    90    69         http://rumahdijual.com/depok/1202967-rumah-minimalis-mewah-murah-di-depok-permata-cimanggis-onyx.html
    123    90    45         http://rumahdijual.com/depok/1202975-rumah-minimalis-mewah-murah-di-depok-permata-cimanggis-onyx.html
    123    84    45         http://rumahdijual.com/depok/1202983-rumah-minimalis-mewah-murah-di-depok-permata-cimanggis-onyx.html
    125    102   45         http://rumahdijual.com/depok/919454-over-kredit-rumah-murah-di-daerah-sawangan-lokasi-strategis.html 
    125    73    47         http://rumahdijual.com/depok/1051165-over-kredit-rumah-di-rtm-cimanggis-depok.html                   
    130    90    45         http://rumahdijual.com/depok/1314684-over-kredit-acacia-gdc-45-90-a.html                             
    130    64    64         http://rumahdijual.com/depok/1064599-rumah-murah-di-pitara.html                                      
    135    60    45         http://rumahdijual.com/depok/1253432-rumah-murah-dilelang-kondisi-apa-adanya-dekat-mal-dtc.html      
    140    104   70         http://rumahdijual.com/depok/1017367-dijul-rmh-over-kredit-di-bedahan-sawangan.html                  
    140    60    60         http://rumahdijual.com/depok/1256865-rumah-murah-2-lantai-di-cilangkap-depok-dekat-dengan.html       
    140    60    60         http://rumahdijual.com/depok/874285-rumah-cluster-citayam-lokasi-strategis-15-ke-stasiun.html        
    145    120   60         http://rumahdijual.com/depok/1135602-dijual-murah-over-kredit-rumah.html                             
    145    65    65         http://rumahdijual.com/depok/1167408-semakin-di-tunda-semakin-mahal.html                             
    150    104   45         http://rumahdijual.com/depok/1053850-di-jual-rumah-second-siap-huni.html                             
    150    102   80         http://rumahdijual.com/depok/967886-rumah-murah-take-over-di-widia-residence-sawangan-depok.html     
    150    92    62         http://rumahdijual.com/depok/1262176-jual-rumah-murah.html                                           
    150    84    43         http://rumahdijual.com/depok/1127263-over-kredit-rumah-siap-huni-tamansari-puri-bali-bojongsari.html 
    150    79    43         http://rumahdijual.com/depok/1263860-dijual-rumah-take-over-di-perum-sawangan-residence-ideal.html   
    150    60    45         http://rumahdijual.com/depok/1281428-rumah-baru-lokasi-nyaman-di-citayam-buaran.html                 
    150    60    45         http://rumahdijual.com/depok/1264571-rumah-baru-lokasi-nyaman-di-citayam.html                        
    155    65    65         http://rumahdijual.com/depok/1066099-tidak-usah-nunggu-pebangunan-lagi-ini-siap-huni.html            
    157    108   50         http://rumahdijual.com/depok/826561-rumah-baru-minimalis-dekat-stasiun-citayam.html
    


```python
selectModerate(df, avg, unit)
```

    
    MODERATE PRICE
    -----------------
    is when the price is above average: 159 (million IDR) with above-average land: 55 (square meters) and above-average building: 40 (square meters)
    
    
    There are : 293  items with above-average price and above-average land.
    
    There are : 223  items with above-average price, above-average land and above-average building.
    
    price  land  building                                                                                                      url
    160    103   75         http://rumahdijual.com/depok/811366-rumah-murah-dicitayam-pabuaran-dekat-stasiun-citayam-10-menit.html
    160    96    48         http://rumahdijual.com/depok/1278622-dijual-cepat-rumah-murah-depok.html                              
    160    70    50         http://rumahdijual.com/depok/853187-dijual-rumah-baru-hanya-3-unit.html                               
    160    65    60         http://rumahdijual.com/depok/1102129-dijual-rumah-sederhana-nan-sejuk.html                            
    160    65    60         http://rumahdijual.com/depok/1102146-dijual-rumah-sederhana-nan-sejuk.html                            
    160    60    60         http://rumahdijual.com/depok/1124488-kapan-lagi-anda-miliki-rumah-mewah-harga-bawah.html              
    160    60    60         http://rumahdijual.com/depok/1134481-sangat-cocok-dengan-anda-yang-sedang-mencari-rumah-dekat.html    
    160    60    60         http://rumahdijual.com/depok/1154444-rumah-murah-di-cluster-citayam-depok.html                        
    160    60    60         http://rumahdijual.com/depok/1154553-rumah-murah-dan-lokasi-strategis-susukan.html                    
    160    55    55         http://rumahdijual.com/depok/1087484-rumah-lt-55-lb-55-di-jual-di-cilangkap.html                      
    165    100   80         http://rumahdijual.com/depok/853162-rumah-dijual-dilingkungan-hijau.html                              
    165    84    45         http://rumahdijual.com/depok/1210920-rumah-dijual-over-credit.html                                    
    165    74    40         http://rumahdijual.com/depok/1150866-rumah-teras.html                                                 
    165    72    45         http://rumahdijual.com/depok/953488-rumah-siap-huni-di-kalimulya-r21-0261-a.html                      
    165    70    45         http://rumahdijual.com/depok/1270391-rumah-murah-jalan-motor-di-pondok-rajeg-r21-0460-a.html          
    165    70    40         http://rumahdijual.com/depok/784138-rumah-minimalis.html                                              
    165    70    40         http://rumahdijual.com/depok/782749-rumah-kita.html                                                   
    165    70    40         http://rumahdijual.com/depok/781073-rumah-tergantung-selera-anda.html                                 
    165    70    40         http://rumahdijual.com/depok/779754-rumah-cantik-menawan.html                                         
    165    70    40         http://rumahdijual.com/depok/777813-rumah-ku.html                                                     
    165    70    40         http://rumahdijual.com/depok/777582-rumah-mu.html                                                     
    165    70    40         http://rumahdijual.com/depok/1299318-rumah-indent-proses-dan-ready-stock.html                         
    165    70    40         http://rumahdijual.com/depok/1294857-rumah-cerdas.html                                                
    165    70    40         http://rumahdijual.com/depok/1252370-rumah-prospek.html                                               
    165    70    40         http://rumahdijual.com/depok/1248667-rumah-montok.html                                                
    165    70    40         http://rumahdijual.com/depok/1233800-rumah-geboy.html                                                 
    165    70    40         http://rumahdijual.com/depok/1247921-rumah-gemol.html                                                 
    165    70    40         http://rumahdijual.com/depok/785419-rumah-cinta.html                                                  
    165    70    40         http://rumahdijual.com/depok/1127279-rumah-warna.html                                                 
    165    70    40         http://rumahdijual.com/depok/1064166-rumah-cerdas.html                                                
    165    70    40         http://rumahdijual.com/depok/1093045-rumah-cakep.html                                                 
    165    70    40         http://rumahdijual.com/depok/1087529-rumah-terdepan.html                                              
    165    70    40         http://rumahdijual.com/depok/1086232-rumah-menerang.html                                              
    165    70    40         http://rumahdijual.com/depok/1086182-ruamh-tinggal.html                                               
    165    70    40         http://rumahdijual.com/depok/1083624-rumah-dingin.html                                                
    165    70    40         http://rumahdijual.com/depok/1082517-rumah-sinar.html                                                 
    165    70    40         http://rumahdijual.com/depok/1076553-rumah-pintar.html                                                
    165    70    40         http://rumahdijual.com/depok/1074564-rumah-setia.html                                                 
    165    70    40         http://rumahdijual.com/depok/1073886-rumah-bersih.html                                                
    165    70    40         http://rumahdijual.com/depok/1072807-rumah-enjoy.html                                                 
    165    70    40         http://rumahdijual.com/depok/1072179-rumah-pugar.html                                                 
    165    70    40         http://rumahdijual.com/depok/785621-rumah-masa-kini.html                                              
    165    70    40         http://rumahdijual.com/depok/1061648-rumah-bening.html                                                
    165    70    40         http://rumahdijual.com/depok/1061111-rumah-jernih.html                                                
    165    70    40         http://rumahdijual.com/depok/1098717-rumah-super.html                                                 
    165    70    40         http://rumahdijual.com/depok/788651-rumah-menawan.html                                                
    165    70    40         http://rumahdijual.com/depok/820582-rumah-keluarga-bahagia.html                                       
    165    70    40         http://rumahdijual.com/depok/792967-rumah-murah-berkualitas.html                                      
    165    70    40         http://rumahdijual.com/depok/956616-rumah-ideal.html                                                  
    165    70    40         http://rumahdijual.com/depok/949606-rumah-meriah.html                                                 
    165    70    40         http://rumahdijual.com/depok/946428-rumah-ramah-tamah.html                                            
    165    70    40         http://rumahdijual.com/depok/925483-rumah-sejuk.html                                                  
    165    70    40         http://rumahdijual.com/depok/868705-rumah-adem-ayem.html                                              
    165    70    40         http://rumahdijual.com/depok/868700-rumah-terbaru.html                                                
    165    70    40         http://rumahdijual.com/depok/846153-rumah-siap-huni.html                                              
    165    70    40         http://rumahdijual.com/depok/832274-rumah-anggun.html                                                 
    165    70    40         http://rumahdijual.com/depok/832267-rumah-idola.html                                                  
    165    70    40         http://rumahdijual.com/depok/828605-rumah-montok.html                                                 
    165    70    40         http://rumahdijual.com/depok/825884-rumah-riang.html                                                  
    165    70    40         http://rumahdijual.com/depok/825843-rumah-ceria.html                                                  
    165    70    40         http://rumahdijual.com/depok/820606-rumah-si-buah-hati.html                                           
    165    70    40         http://rumahdijual.com/depok/819064-rumah-ganteng.html                                                
    165    70    40         http://rumahdijual.com/depok/819059-rumah-tampan.html                                                 
    165    70    40         http://rumahdijual.com/depok/812501-rumah-tablon.html                                                 
    165    70    40         http://rumahdijual.com/depok/812498-rumah-molek.html                                                  
    165    70    40         http://rumahdijual.com/depok/812168-rumah-jangkis.html                                                
    165    70    40         http://rumahdijual.com/depok/811664-rumah-demplon.html                                                
    165    70    40         http://rumahdijual.com/depok/811083-rumah-modis.html                                                  
    165    70    40         http://rumahdijual.com/depok/811065-rumah-selera-anda.html                                            
    165    70    40         http://rumahdijual.com/depok/810844-rumah-indah.html                                                  
    165    70    40         http://rumahdijual.com/depok/808269-rumah-simple.html                                                 
    165    70    40         http://rumahdijual.com/depok/794734-rumah-strategis.html                                              
    165    70    40         http://rumahdijual.com/depok/791615-rumah-impian.html                                                 
    165    65    60         http://rumahdijual.com/depok/1243235-rumah-bagus-type-60-65-di-banjaran-pucung-cilangkap.html         
    165    65    45         http://rumahdijual.com/depok/1155091-bu-di-jual-rumah-di-pancoran-mas-depok-st.html                   
    165    62    55         http://rumahdijual.com/depok/831368-rumah-bagus-siap-huni-dekat-stasiun-citayam.html                  
    165    60    60         http://rumahdijual.com/depok/921689-rumah-lt-60-lb-60-di-jatijajar-depok-siap.html                    
    165    60    50         http://rumahdijual.com/depok/831318-rumah-bagus-siap-huni-lokasi-strategis-disusukan-bojong-gede.html 
    165    60    50         http://rumahdijual.com/depok/728134-rumah-lt-60-lb-50-di-cilangkap-depok-siap.html                    
    165    55    55         http://rumahdijual.com/depok/1309949-rumah-siap-huni-shm.html                                         
    165    55    55         http://rumahdijual.com/depok/1298681-kapan-lagi-anda-miliki-rumah-ini-kalo-bukan-sekarang.html        
    165    55    55         http://rumahdijual.com/depok/1291489-rumah-siap-huni-shm.html                                         
    165    55    55         http://rumahdijual.com/depok/1291393-rumah-siap-huni-shm-bebas-banjir.html                            
    165    55    55         http://rumahdijual.com/depok/1291222-rumah-siap-huni-shm.html                                         
    165    55    55         http://rumahdijual.com/depok/1289348-rumah-siap-huni-shm.html                                         
    165    55    55         http://rumahdijual.com/depok/1285418-rumah-siap-huni-shm-_.html                                       
    165    55    55         http://rumahdijual.com/depok/1285212-rumah-siap-huni-shm.html                                         
    165    55    55         http://rumahdijual.com/depok/1285065-rumah-siap-huni-shm.html                                         
    165    55    55         http://rumahdijual.com/depok/1284945-rumah-siap-huni-shm.html                                         
    165    55    55         http://rumahdijual.com/depok/1283758-rumah-siap-huni-shm.html                                         
    165    55    55         http://rumahdijual.com/depok/1280881-hunian-idaman-keluarga-citayam.html                              
    165    55    55         http://rumahdijual.com/depok/1285495-rumah-siap-huni-shm.html                                         
    165    55    55         http://rumahdijual.com/depok/1185245-rumah-murah-kemana2-cuma-selangkah.html                          
    165    55    55         http://rumahdijual.com/depok/1278489-rumah-citayam-minimalis-shm.html                                 
    165    55    55         http://rumahdijual.com/depok/1062031-cluster-siap-huni-unit-terbatas-buruann.html                     
    165    55    55         http://rumahdijual.com/depok/1071804-rumah-paling-murah-se-citayam-yang-lain-mahalll.html             
    165    55    55         http://rumahdijual.com/depok/1096925-beli-rumah-jangan-asal-murah-nanti-nyesel-kalau-cepat.html       
    165    55    55         http://rumahdijual.com/depok/1103963-hunian-nyaman-bagus-citayam-harga-passss.html                    
    165    55    55         http://rumahdijual.com/depok/1112080-dijual-rumah-dengan-harga-murah-lokasi-strategis.html            
    165    55    55         http://rumahdijual.com/depok/1180179-rumah-dekat-stasiun-citayam-minimalist-harga-terjangkau.html     
    165    55    55         http://rumahdijual.com/depok/1062075-rumah-nyaman-siap-huni.html                                      
    170    87    87         http://rumahdijual.com/depok/1270866-rumah-di-daerah-pekapuran-cimanggis.html                         
    170    85    45         http://rumahdijual.com/depok/960909-over-kredit-rumah-asri-siap-huni-pondok-rajeg-292-a.html          
    170    78    45         http://rumahdijual.com/depok/880285-over-kredit-rumah-minimalis-bumi-sentosa-cibinong-240-a.html      
    170    72    42         http://rumahdijual.com/depok/1168499-take-over-kredit-rumah-tipe-42-72-griya-melati.html              
    170    70    60         http://rumahdijual.com/depok/1153045-rumah-murah-dicipayung-depok.html                                
    170    60    55         http://rumahdijual.com/depok/1146284-dijual-rumah-di-depok.html                                       
    170    60    40         http://rumahdijual.com/depok/931510-rumah-indah-depok.html                                            
    170    56    45         http://rumahdijual.com/depok/877068-rumah-depok-minimalis.html                                        
    170    55    40         http://rumahdijual.com/depok/426354-rumah-murah-dekat-stasiun-depok-dekat-margonda-dekat-gdc.html     
    175    102   80         http://rumahdijual.com/depok/1076518-rumah-dijual-depok-sawangan.html                                 
    175    100   45         http://rumahdijual.com/depok/1230065-rumah-murah-di-depok-over-kredit-r21-0432-a.html                 
    175    90    50         http://rumahdijual.com/depok/1058258-cluster-cantik-di-grand-depok-city-take-over-r21.html            
    175    85    85         http://rumahdijual.com/depok/1281150-rumah-murah-dekat-smp6-kalibaru8-depok.html                      
    175    84    46         http://rumahdijual.com/depok/1296900-jual-cepat-over-kredit-rumah-cluster-curug-residence-2-a.html    
    175    80    45         http://rumahdijual.com/depok/1093864-kredit-tanpa-bunga.html                                          
    175    75    75         http://rumahdijual.com/depok/1167854-hunian-ready-stok-harga-murah-unit-terbatas.html                 
    175    75    75         http://rumahdijual.com/depok/1309914-beli-rumah-di-sini-aja-dijamin-gak-bakalan-galau.html            
    175    70    40         http://rumahdijual.com/depok/1118345-rumah-murah-strategis-ayo-sebelum-harga-property-naik.html       
    175    70    40         http://rumahdijual.com/depok/1118350-rumah-hunian-terbaik-ayo-tahun-depan-property-naik-buruan.html   
    175    66    66         http://rumahdijual.com/depok/950870-rumah-baru-tinggal-finishing-di-kp-bulak-cilodong-depok.html      
    175    66    60         http://rumahdijual.com/depok/1200019-rumah-di-jual-citayem-depok-bogor.html                           
    175    65    56         http://rumahdijual.com/depok/1127400-rumah-minimalis-harga-ekonomis-tipe-56-65-di-jatijajar.html      
    175    60    60         http://rumahdijual.com/depok/1083373-rumah-mewah-lokasi-strategis-harga-irit.html                     
    175    60    60         http://rumahdijual.com/depok/1094639-rumah-lokasi-pas-spesifikasi-teratas-citayam.html                
    175    60    60         http://rumahdijual.com/depok/1100316-beli-rumah-yang-jelas-dan-pasti2-aja-bu-pak.html                 
    175    60    60         http://rumahdijual.com/depok/1194849-rumah-murah-kualitas-gak-murahan.html                            
    175    60    60         http://rumahdijual.com/depok/1216656-rumah-dengan-banyak-keuntungan-nya.html                          
    175    60    60         http://rumahdijual.com/depok/1180180-rumah-murah-citayam-lokasi-strategis.html                        
    175    60    60         http://rumahdijual.com/depok/1065982-rumah-murah-ready-stock-gk-pake-nunggu-nunggu-pembangunan.html   
    175    60    50         http://rumahdijual.com/depok/1135676-rumah-di-cipayung-depok.html                                     
    175    58    45         http://rumahdijual.com/depok/1312190-hunian-terbaru-dikelilingi-perumahan.html                        
    175    58    45         http://rumahdijual.com/depok/1299595-hunian-ready-stock-shm.html                                      
    175    58    45         http://rumahdijual.com/depok/1311958-hunian-terbaru-dikelilingi-perumahan.html                        
    175    58    45         http://rumahdijual.com/depok/1311796-hunian-terbaru-dikelilingi-perumahan.html                        
    175    58    45         http://rumahdijual.com/depok/1298729-cluster-terbaru-pabuaran-shm.html                                
    175    58    45         http://rumahdijual.com/depok/1298345-jangan-survey-lokasi-ini-nanti-kemana2-serba-deket.html          
    175    58    45         http://rumahdijual.com/depok/1298290-hunian-terbaru-nempel-pesona-citayam.html                        
    175    58    45         http://rumahdijual.com/depok/1312120-rumah-idaman-keluarga-citayam-murah-shm.html                     
    175    58    45         http://rumahdijual.com/depok/1292538-hunian-nyaman-dan-ter-baru-di-citayam-pabuaran.html              
    175    58    45         http://rumahdijual.com/depok/1289480-rumah-terlaris-di-pabuaran-susukan-citayam.html                  
    176    65    55         http://rumahdijual.com/depok/943788-rumah-cantik-menarik-di-pitara-depok.html                         
    180    122   47         http://rumahdijual.com/depok/1160797-rumah-aman-nyaman.html                                           
    180    120   90         http://rumahdijual.com/depok/853218-dijual-rumah-dilingkungan-perkampungan.html                       
    180    100   45         http://rumahdijual.com/depok/892353-rumah-sederhana-pribadi-nyaman-depok-jawa-barat.html              
    180    72    72         http://rumahdijual.com/depok/1303446-rumah-murah-kalimulya-dekat-grand-depok-city.html                
    180    72    50         http://rumahdijual.com/depok/897695-rumah-bagus-over-kredit-gdc-anyelir-1-245-a.html                  
    180    65    45         http://rumahdijual.com/depok/1204161-50-meter-ke-jalan-raya-rumah-murah-siap-huni.html                
    180    60    60         http://rumahdijual.com/depok/920891-rumah-di-jual-cepat-murah-lembah-griya-citayam.html               
    180    60    50         http://rumahdijual.com/depok/1120472-rumah-sederhana-di-cinangka-sawangan-depok.html                  
    180    60    40         http://rumahdijual.com/depok/991824-rumah-harga-miring.html                                           
    180    56    45         http://rumahdijual.com/depok/1011595-di-jual-rumah-siap-huni-di-kawasan-kp-utan.html                  
    185    160   63         http://rumahdijual.com/depok/957749-rumah-lt-160-lb-63-di-cilangkap-depok-sebelum.html                
    185    85    85         http://rumahdijual.com/depok/1081498-murah-nyaman-mewah-kemana-mana-serba-deket.html                  
    185    85    85         http://rumahdijual.com/depok/1084697-rumah-memukau-harga-terjangkau.html                              
    185    85    85         http://rumahdijual.com/depok/1180244-rumah-jual-minimalis-harga-manis.html                            
    185    85    85         http://rumahdijual.com/depok/1185249-cluster-nyaman-harga-teman-lokasi-pinggir-jalan.html             
    185    84    50         http://rumahdijual.com/depok/915695-jual-rumah-murah-di-jl-sukatani-bedahan-sawangan-depok.html       
    185    72    45         http://rumahdijual.com/depok/1134957-rumah-minimalis-lokasi-strategis-15-menit-dari-margonda.html     
    185    70    42         http://rumahdijual.com/depok/1275345-rumah-minimalis-3-menit-dari-pacar-citayam.html                  
    185    60    50         http://rumahdijual.com/depok/1020934-sekali-lihat-langsung-cocok.html                                 
    185    60    50         http://rumahdijual.com/depok/1012785-rumah-185-juta-lokasi-dekat-stasiun.html                         
    185    60    42         http://rumahdijual.com/depok/1283626-1-bidang-tanah-60m2-siap-bangun-rumah-sederhana-dirawadenok.html 
    185    60    40         http://rumahdijual.com/depok/1035306-rumah-di-pitara-depok-lt-60m-lb-40m.html                         
    190    100   80         http://rumahdijual.com/depok/734939-jual-rumah-sederhana-bedahan-sawangan-depok.html                  
    190    70    50         http://rumahdijual.com/depok/709254-rumah-bagus-siap-huni-dekat-stasiun-citayam.html                  
    190    60    42         http://rumahdijual.com/depok/1208226-rumah-idaman-murah-lokasi-strategis.html                         
    190    56    56         http://rumahdijual.com/depok/891454-dijual-rumah-murah-cilodong.html                                  
    195    97    45         http://rumahdijual.com/depok/969356-over-kredit-townhouse-siap-huni-masih-mulus-di-kalimulya.html     
    195    80    80         http://rumahdijual.com/depok/874280-rumah-murah-terlaris.html                                         
    195    75    60         http://rumahdijual.com/depok/1158457-butuh-uang-cepat-dijual-take-over-murah-rumah-baru.html          
    195    72    60         http://rumahdijual.com/depok/1176676-dijual-cepat-rumah-beserta-isinya.html                           
    195    72    45         http://rumahdijual.com/depok/1227377-rumah-strategis-di-citayam-depok.html                            
    195    72    45         http://rumahdijual.com/depok/1245581-rumah-strategis-di-citayam-depok.html                            
    195    72    45         http://rumahdijual.com/depok/1245591-rumah-asri-lokasi-strategis-di-citayam-depok.html                
    195    72    45         http://rumahdijual.com/depok/1247495-rumah-asri-lokasi-strategis-di-citayam-depok.html                
    195    72    45         http://rumahdijual.com/depok/1247527-rumah-asri-dan-ntaman-lokasi-strategis-di-citayam-depok.html     
    195    72    45         http://rumahdijual.com/depok/1247699-rumah-asri-aman-nyaman-lokasi-strategis-di-citayam-depok.html    
    195    70    42         http://rumahdijual.com/depok/1275315-rumah-minimalis-pembayaran-bertahap-lokasi-strategis.html        
    195    70    42         http://rumahdijual.com/depok/1227402-rumah-minimalis-lokasi-depok-citayam-strategis.html              
    195    70    42         http://rumahdijual.com/depok/1271018-rumah-idaman-keluarga-lokasi-strategis.html                      
    195    70    42         http://rumahdijual.com/depok/1275272-rumah-minimalis-depok-citayam-strategis-harga-nego.html          
    195    60    60         http://rumahdijual.com/depok/1119084-rumah-murah-cipayung-jembatan-serong-depok.html                  
    195    60    60         http://rumahdijual.com/depok/1146249-rumah-tergantung-selera-anda.html                                
    195    60    42         http://rumahdijual.com/depok/1300784-rumah-minimalis-depok-citayam-lokasi-strategis.html              
    195    60    42         http://rumahdijual.com/depok/1301122-rumah-murah-lokasi-strategis.html                                
    195    60    42         http://rumahdijual.com/depok/1208254-rumah-5-menit-dari-stasiun-citayam-lokasi-strategis.html         
    199    55    55         http://rumahdijual.com/depok/1255037-rumah-minimalis-islami-dekat-pesantren.html                      
    200    135   115        http://rumahdijual.com/depok/968717-rumah-lt-135-lb-115-di-kp-setu-cilangkap.html                     
    200    120   45         http://rumahdijual.com/depok/1054988-rumah-baru-murah.html                                            
    200    116   100        http://rumahdijual.com/depok/593151-rumah-di-mampang-depok-aman-dan-nyaman.html                       
    200    107   60         http://rumahdijual.com/depok/1190000-rumah-murah-sawangan-permai-dekat-ke-kubah-mas.html              
    200    100   82         http://rumahdijual.com/depok/289623-rumah-baru-di-pasir-putih-depok.html                              
    200    100   80         http://rumahdijual.com/depok/805201-jual-rumah-murah-siap-huni-di-cinangka-sawangan-depok.html        
    200    96    60         http://rumahdijual.com/depok/965112-take-over-cipayung-depok-cagar-alam-d-maple-residence.html        
    200    90    55         http://rumahdijual.com/depok/1025570-rumah-di-cilangkap-depok-lt-90-lb-55-siap.html                   
    200    85    50         http://rumahdijual.com/depok/944180-rumah-di-jatijajar-depok-lt-85-lb-50-siap.html                    
    200    80    60         http://rumahdijual.com/depok/1287330-murah-tanah-luas.html                                            
    200    80    50         http://rumahdijual.com/depok/1109733-rumah-kredit-bayar-nya-suka2.html                                
    200    72    60         http://rumahdijual.com/depok/1108251-jual-cash-take-over-rumah-cinere-resdience-meruyung-limo.html    
    200    72    48         http://rumahdijual.com/depok/941780-grand-depok-city-over-kredit-full-furnished.html                  
    200    70    45         http://rumahdijual.com/depok/1252585-rumah-cantik-depok-citayam.html                                  
    200    70    42         http://rumahdijual.com/depok/1224692-rumah-strategis-citayam-idaman-keluarga.html                     
    200    70    40         http://rumahdijual.com/depok/1173641-rumah-dekat-stasiun-bs-cicil-tnp-bank-tnp-bunga.html             
    200    70    40         http://rumahdijual.com/depok/1173646-rumah-nyaman-cicilan-sesuai-kemampuan.html                       
    200    70    40         http://rumahdijual.com/depok/1179986-runah-dgn-cicilan-suka-suka.html                                 
    200    70    40         http://rumahdijual.com/depok/1182362-rumah-strategis-cicilan-manis.html                               
    200    70    40         http://rumahdijual.com/depok/1228441-rumah-mudah-dijangkau.html                                       
    200    70    40         http://rumahdijual.com/depok/571837-cari-rumah-murah.html                                             
    200    65    40         http://rumahdijual.com/depok/1233233-rumah-murah-di-depok.html                                        
    200    65    40         http://rumahdijual.com/depok/437415-rumah-akses-langsung-menuju-stasiun-berhadiah-tv-led-32-a.html    
    200    62    54         http://rumahdijual.com/depok/728062-dijual-rumah-baru-di-depok-samping-maharaja.html                  
    200    60    55         http://rumahdijual.com/depok/1146291-dijual-rumah-di-depok.html                                       
    200    60    40         http://rumahdijual.com/depok/1047053-rumah-lingkungan-nyaman.html                                     
    200    60    40         http://rumahdijual.com/depok/1038846-rumah-murah-kokoh.html                                           
    200    60    40         http://rumahdijual.com/depok/1040245-rumah-cluster-nyaman.html                                        
    200    60    40         http://rumahdijual.com/depok/1119818-rumah-mewah-harga-rendah-di-depok.html                           
    200    60    40         http://rumahdijual.com/depok/1228440-rumah-murah.html                                                 
    200    60    40         http://rumahdijual.com/depok/533394-cluster-griya-cipayung-asri-dkt-stasiun-angkot-24jam.html         
    200    60    40         http://rumahdijual.com/depok/1228442-rumah-murah.html                                                 
    200    60    40         http://rumahdijual.com/depok/533619-rumah-pinggir-jalan-harga-pinggir-hutan.html                      
    200    58    40         http://rumahdijual.com/depok/1061697-rumah-mudah-kemana-mana.html                                     
    200    55    40         http://rumahdijual.com/depok/1127313-rumah-murah-di-depok.html
    


```python
selectExpensive(df, avg, unit)
```

    
    EXPENSIVE PRICE
    -----------------
    is when the price is above average: 159 (million IDR) but you only get land below average: 55 (square meters) and building below average: 40 (square meters).
    
    
    
    There are : 231  items that matched the EXPENSIVE category.
    
    price  land  building                                                                                                         url
    160    50    27         http://rumahdijual.com/depok/1157583-griya-mempesona-harga-terpercaya.html                               
    160    50    27         http://rumahdijual.com/depok/1192397-rumah-non-subsidi-kredit-tanpa-bunga.html                           
    160    50    27         http://rumahdijual.com/depok/1197518-bulan-mudah-punya-rumah.html                                        
    160    50    27         http://rumahdijual.com/depok/1199834-rumah-dengan-banyak-keuntungan.html                                 
    160    50    27         http://rumahdijual.com/depok/1150000-rumah-super-murah-hemat-biaya.html                                  
    160    50    27         http://rumahdijual.com/depok/1130495-minimalis-harga-di-bawah-pasaran.html                               
    160    50    27         http://rumahdijual.com/depok/1121064-rumah-elok-termurah-di-kota-depok.html                              
    160    50    27         http://rumahdijual.com/depok/1124568-rumah-50-ke-akses-jalur-angkot.html                                 
    160    50    27         http://rumahdijual.com/depok/1056634-rumah-idaman-keluarga.html                                          
    160    50    27         http://rumahdijual.com/depok/1063529-cluster-architeria-tipe-27-50-a.html                                
    160    50    27         http://rumahdijual.com/depok/1064532-cluster-architeria-rumah-murah-meriah-dp-bisa-di-cicil.html         
    160    50    27         http://rumahdijual.com/depok/1067807-rumah-minimalis-akses-transport-mudah.html                          
    160    50    27         http://rumahdijual.com/depok/1090682-rumah-promo-akhir-tahun-di-jamin-bebas-banjir.html                  
    160    50    27         http://rumahdijual.com/depok/1092999-rumah-murah-harga-bersahabat.html                                   
    160    50    27         http://rumahdijual.com/depok/1098879-rumah-minimalius-mobil-bisa-masuk.html                              
    160    50    27         http://rumahdijual.com/depok/1119070-rumah-termutrah-di-kota-depok.html                                  
    160    50    27         http://rumahdijual.com/depok/1101961-rumah-murah-masa-depan-keluarga.html                                
    160    50    27         http://rumahdijual.com/depok/1107085-rumah-baru-siap-huni-di-depok.html                                  
    160    50    27         http://rumahdijual.com/depok/1110647-kredit-rumah-tanpa-bunga-murah-depok.html                           
    160    50    27         http://rumahdijual.com/depok/1115288-rumah-indent-request-bisa-disain-sendiri.html                       
    160    50    27         http://rumahdijual.com/depok/1118969-hunian-cluster-berbagai-type.html                                   
    160    50    27         http://rumahdijual.com/depok/1057431-tahun-baru-rumah-baru.html                                          
    160    50    21         http://rumahdijual.com/depok/1306706-cluster-impian-harga-miringan.html                                  
    160    50    21         http://rumahdijual.com/depok/1308657-minimalis-cendrawasih-harga-di-bawah-pasaran.html                   
    160    50    21         http://rumahdijual.com/depok/1311496-rumah-huni-cocok-investasi-depok.html                               
    160    50    21         http://rumahdijual.com/depok/1311549-rumah-berseri-bebas-banjir.html                                     
    160    50    21         http://rumahdijual.com/depok/1311582-rumah-menguntungkan-lokasi-sangat-strategis.html                    
    160    50    21         http://rumahdijual.com/depok/1314342-rumah-ready-stock-dan-indent.html                                   
    160    50    21         http://rumahdijual.com/depok/1314367-cluster-cendrawasih-masih-tersisa-3unit-lagi.html                   
    160    50    21         http://rumahdijual.com/depok/1314447-cendraeasih-bernuansa-alam-indah.html                               
    160    50    21         http://rumahdijual.com/depok/1311512-segera-daptkan-rumah-impian-anda-dengan-harga-murah.html            
    162    36    27         http://rumahdijual.com/depok/954593-green-mini-house-ratujaya-depok-hunian-asri-nyaman-lokasi.html       
    165    50    36         http://rumahdijual.com/depok/900731-rumah-murah-15-menit-ke-stasiun-di-cilodong-siap.html                
    165    50    27         http://rumahdijual.com/depok/888489-rumah-modern-tipe-27-50-mutiara-tapos-depok.html                     
    165    50    21         http://rumahdijual.com/depok/973787-rumah-minimalis-masa-kini.html                                       
    165    50    21         http://rumahdijual.com/depok/947301-rumah-minimalis-angsuran-ringan.html                                 
    165    50    21         http://rumahdijual.com/depok/942444-cluster-cendrawasih-rumah-minimalis-harga-ekonomis.html              
    165    50    21         http://rumahdijual.com/depok/940472-rumah-cantik-depok.html                                              
    165    50    21         http://rumahdijual.com/depok/939270-rumah-murah-harga-ramah.html                                         
    165    50    21         http://rumahdijual.com/depok/939215-rumah-cantik-harga-menarik.html                                      
    165    50    21         http://rumahdijual.com/depok/939188-rumah-bagus.html                                                     
    165    50    21         http://rumahdijual.com/depok/768396-rumah-baru-di-cilodong.html                                          
    165    50    21         http://rumahdijual.com/depok/768218-rumah-keluarga-berencana.html                                        
    165    50    21         http://rumahdijual.com/depok/768194-rumah-baru-lokasi-strategis.html                                     
    165    50    21         http://rumahdijual.com/depok/765508-hunian-baru-bebas-banjir.html                                        
    165    50    21         http://rumahdijual.com/depok/763835-rumah-bebas-banjir.html                                              
    165    50    21         http://rumahdijual.com/depok/760200-rumah-idaman-keluarga.html                                           
    165    50    21         http://rumahdijual.com/depok/632055-rumah-stock-terbatas-di-depok.html                                   
    165    50    21         http://rumahdijual.com/depok/626101-rumah-baru-di-depok.html                                             
    165    50    21         http://rumahdijual.com/depok/476553-rumah-baru-depan-smp-06-cilodong.html                                
    165    50    21         http://rumahdijual.com/depok/1061365-cluster-cendrawasih-minialis-harga-fantastis.html                   
    165    50    21         http://rumahdijual.com/depok/1051262-rumah-cantik-harga-menarik.html                                     
    165    50    21         http://rumahdijual.com/depok/1049656-kangkah-mudah-punya-rumah.html                                      
    165    50    21         http://rumahdijual.com/depok/1048020-rumah-minimalis-deket-stasiun-depok-lama.html                       
    165    50    21         http://rumahdijual.com/depok/1043969-jual-rumah-bagus-harga-mulai-100jt.html                             
    165    50    21         http://rumahdijual.com/depok/1007858-rumah-minimalis-idaman-keluarga-harga-murah.html                    
    165    50    21         http://rumahdijual.com/depok/1006791-perumahan-dicilodong-type-cluster.html                              
    165    50    21         http://rumahdijual.com/depok/760186-rumah-baru-di-depok.html                                             
    165    34    27         http://rumahdijual.com/depok/901537-green-mini-house-depok-ratujaya.html                                 
    167    50    25         http://rumahdijual.com/depok/1022358-bulak-asri-residence-rumah-claster-unit-terbatas.html               
    170    50    27         http://rumahdijual.com/depok/974040-jatiresidense2-modern-hermonis-elegan.html                           
    170    50    21         http://rumahdijual.com/depok/516328-rumah-type-36-termurah.html                                          
    175    50    36         http://rumahdijual.com/depok/1217410-cilangkap-regency-bangunan-baru-dekat-sekali-dengan-jl-raya.html    
    175    50    36         http://rumahdijual.com/depok/420661-satu-kali-naik-menuju-st-depok-baru.html                             
    175    50    36         http://rumahdijual.com/depok/448202-ready-stock-rumah-type-36-50-depok.html                              
    175    50    36         http://rumahdijual.com/depok/858129-rumah-murah-depok.html                                               
    175    50    27         http://rumahdijual.com/depok/1214958-cilangkap-regency-lokasi-premium-dekat-jl-raya-bogor.html           
    175    50    27         http://rumahdijual.com/depok/1223552-cluster-cilangkap-regency-sisa-1-unit-lagi-rumah-baru.html          
    175    50    21         http://rumahdijual.com/depok/1202970-beli-rumah-bisa-umroh-tanpa-di-undi.html                            
    175    50    21         http://rumahdijual.com/depok/1238116-cluster-terracotta-cilangkap-depok-dp-bisa-diangsur.html            
    175    50    21         http://rumahdijual.com/depok/1250142-cluster-cendrawasih-rumah-baru-siap-huni.html                       
    175    50    21         http://rumahdijual.com/depok/1255763-minimalis-harga-bersahabat.html                                     
    175    50    21         http://rumahdijual.com/depok/1257514-beli-rumah-gratis-2-unit-motor-tanpa-diundi.html                    
    175    50    21         http://rumahdijual.com/depok/1258030-rumah-bernuansa-alam-begitu-sejuk-dan-nyaman.html                   
    175    50    21         http://rumahdijual.com/depok/1271297-rumah-minimalis-termurah.html                                       
    175    50    21         http://rumahdijual.com/depok/1283125-kredit-rumah-tanpa-bunga-dan-tanpa-bank-di-daerah.html              
    175    50    21         http://rumahdijual.com/depok/1245624-cluster-cimanggis-regency-dekat-kemanapundepan-tol-cimanggis.html   
    175    50    21         http://rumahdijual.com/depok/1270313-cluster-cendrawasih-rumah-berfariasi.html                           
    175    40    36         http://rumahdijual.com/depok/1030444-rumah-murah-di-jembatan-serong-depok.html                           
    175    40    30         http://rumahdijual.com/depok/1243935-rumah-murah-pinggir-jalan-raya-bogor-km-40-a.html                   
    175    40    30         http://rumahdijual.com/depok/1245651-rumah-murah-pinggir-jalan-raya-bogor.html                           
    175    40    21         http://rumahdijual.com/depok/1107700-rumah-dijual-bagus-murah-di-meruyung-limo-sawangan-depok.html       
    180    50    36         http://rumahdijual.com/depok/1014099-beli-rumah-dari-pada-ngontrak.html                                  
    180    50    36         http://rumahdijual.com/depok/1211139-rumah-ready-stock-di-kalibaru-cilodong-nempel-sama-gdc.html         
    180    50    21         http://rumahdijual.com/depok/1255529-rumah-ready-stok-samping-gdc.html                                   
    180    50    21         http://rumahdijual.com/depok/1263452-rumah-murah-siap-huni-cilodong.html                                 
    180    50    21         http://rumahdijual.com/depok/1271439-rumah-minimalis-siap-huni.html                                      
    180    50    21         http://rumahdijual.com/depok/1275892-rumah-kebanggaan-keluarga.html                                      
    180    50    21         http://rumahdijual.com/depok/1286708-rumah-baru-tipe-21-50-a.html                                        
    180    50    21         http://rumahdijual.com/depok/1286722-rumah-minimalis-murah.html                                          
    180    50    21         http://rumahdijual.com/depok/1286880-rumah-baru-nasib-baru.html                                          
    180    50    21         http://rumahdijual.com/depok/1262582-rumah-siap-huni-di-depok.html                                       
    180    50    21         http://rumahdijual.com/depok/1301495-cluster-cendrawasih-rumah-berfariasi-siap-huni.html                 
    180    35    30         http://rumahdijual.com/depok/859216-rumah-mungil-harga-ekonomis-di-rangkapan-jaya-pancoran-mas.html      
    185    50    36         http://rumahdijual.com/depok/1052150-rumah-murah-dekat-kemana-mana.html                                  
    185    50    27         http://rumahdijual.com/depok/1040093-rumah-murah-berkualitas-cilodong.html                               
    185    50    27         http://rumahdijual.com/depok/1042470-tahap-5-ready-stock-type-27-50-cilodong.html                        
    185    50    27         http://rumahdijual.com/depok/1046734-cluster-trendy-2015-a.html                                          
    185    50    27         http://rumahdijual.com/depok/1054121-rumah-bebas-bansjir.html                                            
    185    50    27         http://rumahdijual.com/depok/1273000-rumah-impian-keluarga-siap-huni-harga-murah-meriah.html             
    185    50    27         http://rumahdijual.com/depok/974019-rumah-cluster-cendrawasih-cilodong-depok.html                        
    185    50    27         http://rumahdijual.com/depok/974073-rumah-huk-minimalis-cluster-cendrawasih.html                         
    185    50    27         http://rumahdijual.com/depok/1065918-cluster-bintang-5-harga-kaki-5-cilodong-depok.html                  
    185    50    21         http://rumahdijual.com/depok/1254001-rumah-siap-huni-clustr-cendrawasih.html                             
    185    50    21         http://rumahdijual.com/depok/1257387-rumah-siap-huni-di-cluster-cendrawasih.html                         
    185    50    21         http://rumahdijual.com/depok/1272967-cluster-siap-huni-minimalis-harga-fantastis.html                    
    185    50    21         http://rumahdijual.com/depok/1286750-rumah-impian-keluarga-harmonis-siap-huni.html                       
    185    50    21         http://rumahdijual.com/depok/1286757-rumah-minimalis-siap-huni.html                                      
    185    50    21         http://rumahdijual.com/depok/1286763-rumah-bernuansa-alam-begitu-sejuk-dan-nyaman.html                   
    185    35    26         http://rumahdijual.com/depok/992741-dijual-rumah-mungil-di-margonda-depok-stok-terbatas.html             
    190    50    36         http://rumahdijual.com/depok/1094951-rumah-minimalis-murah-meriah.html                                   
    190    50    27         http://rumahdijual.com/depok/1238102-rumah-murah-cluster-terracotta-cilangkap-depok.html                 
    190    40    35         http://rumahdijual.com/depok/1297213-rumah-baru-di-liohek-pondok-terong-depok.html                       
    195    50    36         http://rumahdijual.com/depok/1071139-cluster-nyaman-harga-teman-lokasi-pinggir-jalan.html                
    195    50    36         http://rumahdijual.com/depok/727288-rumah-mewahan-harga-lesehan.html                                     
    195    50    36         http://rumahdijual.com/depok/739958-rumah-cluster-harga-hamster.html                                     
    195    50    36         http://rumahdijual.com/depok/795023-pilihan-tepat-untuk-keluarga-anda.html                               
    195    50    36         http://rumahdijual.com/depok/807090-rumah-murah-lokasi-strategis-model-nya-manis.html                    
    195    50    36         http://rumahdijual.com/depok/811531-sekali-lihat-pasti-cocok-lokasi-oke-banget-dekat-stasiun.html        
    195    50    36         http://rumahdijual.com/depok/815269-sekali-lihat-pasti-cocok.html                                        
    195    50    36         http://rumahdijual.com/depok/831946-sekali-lihat-pasti-cocok.html                                        
    195    50    36         http://rumahdijual.com/depok/853683-taman-jaya-rumah-minimalis.html                                      
    195    50    36         http://rumahdijual.com/depok/729947-rumah-cluster-kota-depok.html                                        
    195    50    30         http://rumahdijual.com/depok/366366-rumah-murah-di-depok-timur.html                                      
    195    50    30         http://rumahdijual.com/depok/372411-cuma-punya-200jt-ingin-rumah-dekat-margonda-yakin-kesini.html        
    195    50    21         http://rumahdijual.com/depok/901042-rumah-minimalis-ready-stok-di-cilodong-depok.html                    
    195    50    21         http://rumahdijual.com/depok/933642-rumah-ready.html                                                     
    195    45    30         http://rumahdijual.com/depok/1051335-lt-45-lb-30-cluster-minimalis-siap-huni.html                        
    195    45    30         http://rumahdijual.com/depok/952497-punya-rumah-bagus-siap-huni-harga-murah.html                         
    195    45    30         http://rumahdijual.com/depok/974318-rumah-ijo-ready-stock.html                                           
    198    50    36         http://rumahdijual.com/depok/845512-rumah-dikota-harga-desa.html                                         
    198    50    36         http://rumahdijual.com/depok/822579-sekali-lihat-pasti-cocok.html                                        
    198    50    30         http://rumahdijual.com/depok/399190-minihouse-juanda-masa-hari-gini-cari-rumah-deket-margonda.html       
    199    50    36         http://rumahdijual.com/depok/1076693-one-gate-system-keamanan-24-jam.html                                
    200    50    36         http://rumahdijual.com/depok/997225-beli-rumah-dapat-mobil.html                                          
    200    50    36         http://rumahdijual.com/depok/997476-cluster-nyaman-harga-teman-lokasi-pinggir-jalan.html                 
    200    50    36         http://rumahdijual.com/depok/997566-stop-beli-rumah-yang-asal-bangun-beli-rumah-disini.html              
    200    50    36         http://rumahdijual.com/depok/1020819-rumah-kota-harga-desa.html                                          
    200    50    36         http://rumahdijual.com/depok/995860-cluster-nyaman-harga-teman-lokasi-pinggir-jalan.html                 
    200    50    36         http://rumahdijual.com/depok/892643-cluster-kota-depok.html                                              
    200    50    36         http://rumahdijual.com/depok/995483-rumah-elit-harga-irit.html                                           
    200    50    36         http://rumahdijual.com/depok/872316-cluster-minimalis-dekat-stasiun-dan-terminal-depok.html              
    200    50    36         http://rumahdijual.com/depok/872827-bumi-rinjani-2-cluster-depok.html                                    
    200    50    36         http://rumahdijual.com/depok/874166-rumah-dijual-cipayung-rumah-kavling-minimalis-dekat-jalur-angkot.html
    200    50    36         http://rumahdijual.com/depok/884168-sekali-lihat-pasti-cocok-lokasi-dekat-stasiun-depok.html             
    200    50    36         http://rumahdijual.com/depok/902802-rumah-kota-harga-desa.html                                           
    200    50    36         http://rumahdijual.com/depok/904545-rumah-kota-harga-desa.html                                           
    200    50    36         http://rumahdijual.com/depok/905128-rumah-cluater-kota-depok-murah-tidak-kpr.html                        
    200    50    36         http://rumahdijual.com/depok/905139-rumah-cluater-kota-depok-murah-tidak-kpr.html                        
    200    50    36         http://rumahdijual.com/depok/910099-cluster-sederhana-bergaya-moderen.html                               
    200    50    36         http://rumahdijual.com/depok/919464-rumah-cluster-harga-wafer-di-pake.html                               
    200    50    36         http://rumahdijual.com/depok/920242-rumah-cluster-taman-jaya.html                                        
    200    50    36         http://rumahdijual.com/depok/932507-jual-cepat-rumah-mewah-harga-murah.html                              
    200    50    36         http://rumahdijual.com/depok/941061-rumah-cluster-type-36-50-a.html                                      
    200    50    36         http://rumahdijual.com/depok/962162-kami-menjual-rumah-cluster-minimalis-dengan-harga-terjangkau-dan.html
    200    50    36         http://rumahdijual.com/depok/995439-rumah-elit-harga-irit.html                                           
    200    50    36         http://rumahdijual.com/depok/995450-cluster-nyaman-harga-teman-lokasi-pinggir-jalan.html                 
    200    50    36         http://rumahdijual.com/depok/995493-sekali-lihat-pasti-cocok.html                                        
    200    50    36         http://rumahdijual.com/depok/867008-taman-jaya-rumah-minimalis.html                                      
    200    50    36         http://rumahdijual.com/depok/863202-sekali-lihat-pasti-cocok.html                                        
    200    50    36         http://rumahdijual.com/depok/1277083-rumah-cluster-depok-lama.html                                       
    200    50    36         http://rumahdijual.com/depok/861210-rumah-cluster-minimalis-baru-di-kota-depok.html                      
    200    50    36         http://rumahdijual.com/depok/1017759-rumah-kota-harga-desa.html                                          
    200    50    36         http://rumahdijual.com/depok/1022488-rumah-mewah-harga-rendah-di-depok.html                              
    200    50    36         http://rumahdijual.com/depok/1024155-cluster-murah-harga-indah.html                                      
    200    50    36         http://rumahdijual.com/depok/1028778-rumah-termurah-sekota-depok-harga-sudah-pasti-anda-cocok.html       
    200    50    36         http://rumahdijual.com/depok/1030403-rumah-nyaman-harga-teman.html                                       
    200    50    36         http://rumahdijual.com/depok/1030583-di-sini-gan-kalau-mau-beli-rumah-murah-dekat.html                   
    200    50    36         http://rumahdijual.com/depok/1040462-rumah-cluster-cuma-200jt-dikota-depok.html                          
    200    50    36         http://rumahdijual.com/depok/1043544-beli-rumah-di-sini-aja-di-sana-mah-mahal.html                       
    200    50    36         http://rumahdijual.com/depok/1048733-rumah-baru-harga-lama-dikota-depok.html                             
    200    50    36         http://rumahdijual.com/depok/1050754-sekali-lihat-pasti-cocok.html                                       
    200    50    36         http://rumahdijual.com/depok/1052161-hunian-bebas-banjir-36-50-kota-depok.html                           
    200    50    36         http://rumahdijual.com/depok/1057412-rumah-depok-banyak-yg-murah-tpi-yg-pasti-disini.html                
    200    50    36         http://rumahdijual.com/depok/1073087-cluster-nyaman-harga-teman-lokasi-pinggir-jalan.html                
    200    50    36         http://rumahdijual.com/depok/1076445-cluster-nyaman-harga-teman-lokasi-pinggir-jalan.html                
    200    50    36         http://rumahdijual.com/depok/1078652-sekali-lihat-pasti-cocok.html                                       
    200    50    36         http://rumahdijual.com/depok/1079853-sekali-lihat-pasti-cocok.html                                       
    200    50    36         http://rumahdijual.com/depok/1083699-sekali-lihat-pasti-cocok.html                                       
    200    50    36         http://rumahdijual.com/depok/1014104-rumh-harga-mobil.html                                               
    200    50    36         http://rumahdijual.com/depok/1085501-sekali-lihat-pasti-cocok.html                                       
    200    50    36         http://rumahdijual.com/depok/1012446-rumah-mantap-harga-sahabat.html                                     
    200    50    36         http://rumahdijual.com/depok/1010077-rumah-elit-harga-irit.html                                          
    200    50    36         http://rumahdijual.com/depok/1009433-sekali-lihat-pasti-cocok.html                                       
    200    50    36         http://rumahdijual.com/depok/1010023-cluster-minimalis-pitara-depok-3-menit-ke-stasiun.html              
    200    50    36         http://rumahdijual.com/depok/1011016-sekali-lihat-pasti-cocok.html                                       
    200    50    36         http://rumahdijual.com/depok/861244-hunian-cantik-lokasi-asik-harga-asik-aman-tidak-berisik.html         
    200    50    36         http://rumahdijual.com/depok/1090158-sekali-lihat-pasti-cocok.html                                       
    200    50    36         http://rumahdijual.com/depok/1121581-rumah-tumbuh-harga-jatuh.html                                       
    200    50    36         http://rumahdijual.com/depok/763601-rumah-cluster-minimalis-depok.html                                   
    200    50    36         http://rumahdijual.com/depok/763602-rumah-murah-akses-dekat-jalan-raya.html                              
    200    50    36         http://rumahdijual.com/depok/794901-cluster-taman-jaya-kota-depok-menyediakan-rumah-yang-harga.html      
    200    50    36         http://rumahdijual.com/depok/804308-sekali-lihat-pasti-cocok.html                                        
    200    50    36         http://rumahdijual.com/depok/806633-cari-rumah-murah-dan-nyaman-disini-tempat-nya.html                   
    200    50    36         http://rumahdijual.com/depok/806648-stop-beli-rumah-yang-asal-bangun-beli-rumah-disini.html              
    200    50    36         http://rumahdijual.com/depok/808933-cluster-bulak-timur-residence-village-depok.html                     
    200    50    36         http://rumahdijual.com/depok/824560-mau-punya-rumah-mau-investasi-disini-tempat-nya.html                 
    200    50    36         http://rumahdijual.com/depok/827113-rumah-cluster-taman-jaya-cipayung-didepok.html                       
    200    50    36         http://rumahdijual.com/depok/831806-cluster-termurah-sekota-depok-lokasi-dekat-stasiun-depok-bebas.html  
    200    50    36         http://rumahdijual.com/depok/832255-cluster-griya-bulak-timur-residence-village-depok.html               
    200    50    36         http://rumahdijual.com/depok/834301-rumah-manis-harga-ga-bikin-anda-nangis.html                          
    200    50    36         http://rumahdijual.com/depok/839403-rumah-cluster-taman-jaya-depok.html                                  
    200    50    36         http://rumahdijual.com/depok/840883-rumah-cluster-kota-depok.html                                        
    200    50    36         http://rumahdijual.com/depok/841231-rumah-murah-kuwalitas-mewah.html                                     
    200    50    36         http://rumahdijual.com/depok/846471-sekali-lihat-pasti-cocok.html                                        
    200    50    36         http://rumahdijual.com/depok/851273-rumah-elit-harga-irit.html                                           
    200    50    36         http://rumahdijual.com/depok/740037-rumah-cluster-depok-bebas-banjir-dekat-stasiun.html                  
    200    50    36         http://rumahdijual.com/depok/1097734-sekali-lihat-pasti-cocok.html                                       
    200    50    36         http://rumahdijual.com/depok/739454-rumah-cluster-minimalis-harga-ekonomis-lokasi-strategis-depok.html   
    200    50    36         http://rumahdijual.com/depok/723803-rumah-dekat-stasiun-depok.html                                       
    200    50    36         http://rumahdijual.com/depok/1125832-rumah-oke-harga-ga-bikin-kantong-boke.html                          
    200    50    36         http://rumahdijual.com/depok/1133443-rumah-murah-kualitas-dan-gak-murahan-di-depok.html                  
    200    50    36         http://rumahdijual.com/depok/1134823-rumah-baru-harga-lama-dikota-depok.html                             
    200    50    36         http://rumahdijual.com/depok/1234877-rumah-pinggir-jalan-200-juta.html                                   
    200    50    36         http://rumahdijual.com/depok/1276744-rumah-cluster-paling-murah.html                                     
    200    50    36         http://rumahdijual.com/depok/1277052-rumah-cluster-murah-meriah.html                                     
    200    50    36         http://rumahdijual.com/depok/1277057-rumah-cluster-sesuai-bajet-keuangan-anda.html                       
    200    50    36         http://rumahdijual.com/depok/1277066-rumah-murah-bergaya-mewah.html                                      
    200    50    36         http://rumahdijual.com/depok/1277088-rumah-cluster-harga-kaget.html                                      
    200    50    36         http://rumahdijual.com/depok/1277107-rumah-cluster-harga-wow.html                                        
    200    50    36         http://rumahdijual.com/depok/1277111-rumah-murah-kualitas-mewah.html                                     
    200    50    36         http://rumahdijual.com/depok/1277122-rumah-cluster-harga-wow.html                                        
    200    50    36         http://rumahdijual.com/depok/1277211-rumah-murah-sesuai-kantong-anda.html                                
    200    50    36         http://rumahdijual.com/depok/1277237-depok-cluster-taman-indah.html                                      
    200    50    36         http://rumahdijual.com/depok/1277240-rumah-cluster-gelora-raya.html                                      
    200    50    36         http://rumahdijual.com/depok/1277251-rumah-cluster-jaya-indah.html                                       
    200    50    36         http://rumahdijual.com/depok/733299-rumah-cluster-murah-dekat-stasiun-depok.html                         
    200    50    35         http://rumahdijual.com/depok/1128153-jangan-beli-rumah-di-sini-karena-dekat-kemana-mana.html             
    200    35    35         http://rumahdijual.com/depok/1104122-apartemen-lotus-residence-grand-depok-city-r21-0398-a.html          
    200    21    30         http://rumahdijual.com/depok/1172344-rumah-di-cimpaeun-tapos-depok.html                                  
    200    5     36         http://rumahdijual.com/depok/997552-rumah-elit-harga-irit.html
    

## House Price Between 300 - 400 Mio IDR

### Visualize Data


```python
df = visualizeData('depok', 300, 400);
```


![png](png/output_32_0.png)


### Analyze the Data of House Price Between 300 - 400 Mio IDR


```python
avg = averageMeasures(df)
```

    
    AVERAGE MEASURES
    -----------------
    
    building    46
        land    80
       price   361
    


```python
mostSpacious(df)
```

    
    MOST SPACIOUS LAND
    -----------------
    
        bath     2
         bed     4
    building   180
        land   500
       price   350
         url   http://rumahdijual.com/depok/1117405-sawangan-depok-jalan-pengasinan.html
    
    MOST SPACIOUS BUILDING
    -----------------
    
        bath     2
         bed     4
    building   180
        land   500
       price   350
         url   http://rumahdijual.com/depok/1117405-sawangan-depok-jalan-pengasinan.html
    


```python
selectEconomical(df, avg, unit)
```

    
    MOST ECONOMICAL
    -----------------
    is when the price is really below average: 361 (million IDR) but you get above the average land: 80 (square meters) and above the average building: 46 (square meters)
    
    You are blessed to choose one of these 154  houses:
    
    price  land building                                                                                                          url
    300     99    99       http://rumahdijual.com/depok/1271851-rumah-minimalis.html                                                 
    300     98    90       http://rumahdijual.com/depok/1073443-dijual-cepat-rumah-harga-300jt-kawasan-depok.html                    
    300     92    80       http://rumahdijual.com/depok/994192-jual-bu-rumah-kontrakan-2-pintu-di-jl-gelatik.html                    
    300     85    65       http://rumahdijual.com/depok/849969-di-jual-rumah-bagus-di-samping-perum-anyelir-2-a.html                 
    300     85    50       http://rumahdijual.com/depok/938575-rumah-depok-citayam-minimalis-lok-strategis-harga-nego.html           
    300     85    50       http://rumahdijual.com/depok/1016686-rumah-idaman-depok-citayam-lokasi-strategis.html                     
    300     85    50       http://rumahdijual.com/depok/1015617-rumah-murah-lokasi-strategis.html                                    
    300     85    50       http://rumahdijual.com/depok/1284475-rumah-minimalis-lokasi-strategis-harga-nego.html                     
    300     85    50       http://rumahdijual.com/depok/1015602-rumah-citayam-20-menit-dari-campus-ui-depok-lokasi.html              
    300     84    60       http://rumahdijual.com/depok/941700-rumah-di-grand-depok-city-r21-0143-over-kredit.html                   
    300     311   100      http://rumahdijual.com/depok/1153133-dijual-murah-tanah-rumah-kontrakan-4-pintu-275juta-nego.html         
    300     300   120      http://rumahdijual.com/depok/1064457-depok-rawa-indah-rumah-sederhana-tanah-luas-nyaman-adem.html         
    300     300   120      http://rumahdijual.com/depok/941171-pondok-terong-rumah-sederhana-tanah-luas.html                         
    300     300   120      http://rumahdijual.com/depok/851389-pondok-terong-rumah-sederhana-tanah-luas-nyaman-adem.html             
    300     220   160      http://rumahdijual.com/depok/981389-sawangan-permai-bu-rumah-di-jual.html                                 
    300     170   150      http://rumahdijual.com/depok/836724-rumah-lt-170-lb-150-di-cilangkap-depan-pesantren.html                 
    300     130   100      http://rumahdijual.com/depok/533573-jual-rumah-murah-bedahan-sawangan-depok.html                          
    300     128   82       http://rumahdijual.com/depok/1044050-over-kredit-cicilan-dp-rumah-lavanya-hills-cinere.html               
    300     127   60       http://rumahdijual.com/depok/1256648-rumah-murah-strategis-di-citayam.html                                
    300     120   100      http://rumahdijual.com/depok/661183-rumah-lt-120-lb-100-di-pinggir-jalan-banjaran.html                    
    300     115   100      http://rumahdijual.com/depok/1051675-rumah-kampng-harga-pas-msuk-mobil-di-rangkapan-jaya.html             
    300     112   97       http://rumahdijual.com/depok/985138-di-jual-rumah-dekat-stasiun-citayam.html                              
    300     107   76       http://rumahdijual.com/depok/1226196-rumah-dijual-dekat-masjid-kubah-mas-sawangan-depok.html              
    300     100   80       http://rumahdijual.com/depok/900099-rumah-murah.html                                                      
    300     100   75       http://rumahdijual.com/depok/802429-rumah-memukau-harga-terjangkau-di-cluster-jatimulya.html              
    300     100   100      http://rumahdijual.com/depok/801927-rumah-warung-lt-100-lb-100-di-cilangkap-depok.html                    
    309     126   54       http://rumahdijual.com/depok/1194455-rumah-dijual-cepat-bedahan-second.html                               
    310     84    54       http://rumahdijual.com/depok/905959-majesty-residence-citayam-cuma-15menit-ke-stasiun-citayam.html        
    310     84    47       http://rumahdijual.com/depok/1174349-rumah-2-lantai-harga-1-lantai-di-kalisuren-dp.html                   
    310     82    82       http://rumahdijual.com/depok/924156-rumah-1-induk-2-kontrakan.html                                        
    310     81    50       http://rumahdijual.com/depok/960575-rumah-sejuta-fasilitas-5-menit-dr-stasiun.html                        
    310     126   54       http://rumahdijual.com/depok/1194347-rumah-dijual-dibedahan-sawangan-kota-depok-second.html               
    310     108   75       http://rumahdijual.com/depok/1039649-dijual-rumah-tinggal.html                                            
    310     105   80       http://rumahdijual.com/depok/788863-rumah-siap-huni-depok.html                                            
    312     90    50       http://rumahdijual.com/depok/474968-rumah-besar-harga-kecil-di-ciseeng-bogor.html                         
    312     120   100      http://rumahdijual.com/depok/1118268-rumah-di-cagar-alam.html                                             
    315     95    60       http://rumahdijual.com/depok/901794-rumah-murah.html                                                      
    315     93    87       http://rumahdijual.com/depok/945949-rumah-rawadenok.html                                                  
    315     84    60       http://rumahdijual.com/depok/922433-rumah-dijual-cepat.html                                               
    319     84    47       http://rumahdijual.com/depok/694217-rumah-elite-2-lantai-di-kalisuren-uang-muka-cuma.html                 
    320     91    70       http://rumahdijual.com/depok/1117329-rumah-baru-dengan-akses-angkot-24-jam-10-menit.html                  
    320     90    90       http://rumahdijual.com/depok/1099286-depot-bumi-sawangan.html                                             
    320     90    70       http://rumahdijual.com/depok/1027179-dijual-rumah-di-bumi-sawangan-indah.html                             
    320     90    50       http://rumahdijual.com/depok/1125960-rumah-murah.html                                                     
    320     85    50       http://rumahdijual.com/depok/978176-griya-sindangkarsa-rumah-ready-stok-2-unit-lagi-buruan.html           
    320     84    60       http://rumahdijual.com/depok/1219462-dijual-rumah-paling-murah-di-gdc-depok.html                          
    320     84    47       http://rumahdijual.com/depok/694240-cari-rumah-2-lantai-tapi-harga-terjangkau-di-phaniisan.html           
    320     81    57       http://rumahdijual.com/depok/1101217-rumah-siap-huni-di-taman-anyelir-1-a.html                            
    320     181   80       http://rumahdijual.com/depok/1221140-jual-rumah-cipayung-depok-harga-murah-bu.html                        
    320     154   84       http://rumahdijual.com/depok/1281903-rumah-murah-300jtan-di-bojong-sari-depok.html                        
    320     150   100      http://rumahdijual.com/depok/1093144-rumah-luas-asri-lt-150m-lb-100m-cipayung-depok.html                  
    320     120   120      http://rumahdijual.com/depok/1254721-kontrakan-4-pintu-di-cilangkap-depok-dekat-lapangan-bdb.html         
    320     100   60       http://rumahdijual.com/depok/1143104-rumah-nyaman-harga-teman-lokasi-strategis.html                       
    325     98    90       http://rumahdijual.com/depok/1244414-di-jual-rumah-lokasi-strategis-bebas-banjir.html                     
    325     97    59       http://rumahdijual.com/depok/1261265-rumah-murah-di-cipayung-depok-kavling-terbatas.html                  
    325     97    59       http://rumahdijual.com/depok/1148674-rumah-murah-siap-huni-di-kp-sempu-cipayung-depok.html                
    325     96    60       http://rumahdijual.com/depok/1243244-di-jual-rumah.html                                                   
    325     90    90       http://rumahdijual.com/depok/1102150-jual-rumah-di-depok.html                                             
    325     84    55       http://rumahdijual.com/depok/862954-rumah-cluster-astri-dan-sejuk.html                                    
    325     154   84       http://rumahdijual.com/depok/1281796-rumah-murah-300-juta-di-curug-bojongsari-depok.html                  
    325     154   84       http://rumahdijual.com/depok/1290054-tanah-rumah-setengah-pembangunan-depok.html                          
    325     150   100      http://rumahdijual.com/depok/836729-rumah-lt-150-lb-100-di-depan-pesantren-darussalam.html                
    325     120   120      http://rumahdijual.com/depok/697572-rumah-kontrakan-buat-investasi-masa-tua.html                          
    325     115   80       http://rumahdijual.com/depok/903643-rumah-bekas-berkualitas.html                                          
    325     100   70       http://rumahdijual.com/depok/737912-rumah-bagus-dekat-gdc-depok.html                                      
    330     81    81       http://rumahdijual.com/depok/710208-djual-cepat-rumah-minimalis-di-sukamaju-depok.html                    
    330     140   100      http://rumahdijual.com/depok/853118-rumah-dijual-2-unit-bisa-beli-satu-satu.html                          
    330     107   90       http://rumahdijual.com/depok/1313874-rumah-di-daerah-strategis-dengan-cicilan-terjangkau-fixed-selama.html
    330     107   90       http://rumahdijual.com/depok/1315014-rumah-dengan-harga-ringan-di-kawasan-strategis-pancoran-mas.html     
    330     104   90       http://rumahdijual.com/depok/724431-rumah-mampang-depok.html                                              
    333     90    75       http://rumahdijual.com/depok/1301138-22-di-jual-rumah-perumnas-depok-timur-harga-terjangkau.html          
    335     100   64       http://rumahdijual.com/depok/1144276-sawangan-lt-100-m2-335-juta.html                                     
    340     97    60       http://rumahdijual.com/depok/1301552-rumah-di-depok-jembatan-serong.html                                  
    340     87    60       http://rumahdijual.com/depok/1134996-dijual-rumah-permanen-siap-huni.html                                 
    340     84    60       http://rumahdijual.com/depok/867284-dijual-cepat-rumah-kalimulya.html                                     
    340     81    50       http://rumahdijual.com/depok/1064932-hunian-nyaman-aman-tentram.html                                      
    340     106   60       http://rumahdijual.com/depok/989896-rumah-cantik-harga-menarik-siap-huni.html                             
    340     105   60       http://rumahdijual.com/depok/995465-rumah-100-siap-huni-depok.html                                        
    340     100   60       http://rumahdijual.com/depok/980887-rumah-siap-huni-lt-105-a.html                                         
    340     100   60       http://rumahdijual.com/depok/980891-rumah-murah-ready-stok-depok.html                                     
    345     85    60       http://rumahdijual.com/depok/852302-rumah-murah-siap-huni-taman-ayelir-1-dekat-gdc.html                   
    350     97    55       http://rumahdijual.com/depok/1205837-rumah-shm-kawasan-strategis-sempu-indah-kota-depok.html              
    350     96    52       http://rumahdijual.com/depok/831251-rumah-lokasi-strategis.html                                           
    350     95    70       http://rumahdijual.com/depok/993220-rumah-murah-di-cipayung-depok-15-mnt-ke-stasiun.html                  
    350     94    65       http://rumahdijual.com/depok/1202852-dijual-cepat-rumah-di-jatijajar-tapos-depok-harga-nego.html          
    350     93    87       http://rumahdijual.com/depok/945951-rumah-rawadenok.html                                                  
    350     92    50       http://rumahdijual.com/depok/1069502-rumah-100-baru-siap-huni-di-depok.html                               
    350     91    91       http://rumahdijual.com/depok/1146437-rumah-murah-di-tengah-kota.html                                      
    350     91    75       http://rumahdijual.com/depok/756133-cluster-cantik-kp-kresek.html                                         
    350     90    80       http://rumahdijual.com/depok/1142729-rumah-dijual-di-citayam-dan-dekat-stasiun.html                       
    350     90    60       http://rumahdijual.com/depok/1286008-hunian-nyaman-dan-asri-di-sawangan.html                              
    350     90    60       http://rumahdijual.com/depok/827972-rumah-cantik-di-grand-depok-city-r21-0227-a.html                      
    350     90    60       http://rumahdijual.com/depok/973103-jual-rumah-di-perumnas-depok-timur.html                               
    350     90    60       http://rumahdijual.com/depok/911091-jangan-mikir-2-kali-lama-mikir-dapat-di-pinggir.html                  
    350     90    50       http://rumahdijual.com/depok/1081344-cluster-ready-stok-cipayung-depok.html                               
    350     90    50       http://rumahdijual.com/depok/1082034-rumah-bebas-banjir-free-biaya-surat.html                             
    350     90    50       http://rumahdijual.com/depok/1077947-rumah-murah-spesial-akhir-tahun.html                                 
    350     90    50       http://rumahdijual.com/depok/1077948-rumah-kualitas-ok-depok.html                                         
    350     90    50       http://rumahdijual.com/depok/1061701-rumah-cluster-free-biaya-surat.html                                  
    350     90    50       http://rumahdijual.com/depok/1054407-cluster-murah-tapi-ga-murahan.html                                   
    350     90    50       http://rumahdijual.com/depok/1054534-rumah-manis-minimalis.html                                           
    350     90    50       http://rumahdijual.com/depok/1058493-rumah-baru-2015-siap-huni-depok.html                                 
    350     87    50       http://rumahdijual.com/depok/917960-rumah-cluster-kota-depok.html                                         
    350     87    50       http://rumahdijual.com/depok/892580-rumah-cluster-kota-depok.html                                         
    350     87    50       http://rumahdijual.com/depok/917948-rumah-cluster-kota-depok.html                                         
    350     85    85       http://rumahdijual.com/depok/1138288-rumah-bagus-murah-depok.html                                         
    350     85    50       http://rumahdijual.com/depok/1101408-rumah-besar-harga-kecil.html                                         
    350     85    50       http://rumahdijual.com/depok/790315-rumah-ready-di-depok.html                                             
    350     84    72       http://rumahdijual.com/depok/42991-jual-rumah-pamulang.html                                               
    350     84    55       http://rumahdijual.com/depok/1069259-rumah-di-cinangka-sawangan-depok.html                                
    350     84    50       http://rumahdijual.com/depok/916125-dijual-rumah-murah-minimalis-di-depok.html                            
    350     84    50       http://rumahdijual.com/depok/1186052-rumah-di-depok-pitara.html                                           
    350     84    50       http://rumahdijual.com/depok/1186585-rumah-dekat-dtc-depok.html                                           
    350     83    83       http://rumahdijual.com/depok/649087-rumah-baru-di-jual.html                                               
    350     500   180      http://rumahdijual.com/depok/1117405-sawangan-depok-jalan-pengasinan.html                                 
    350     160   150      http://rumahdijual.com/depok/890517-bu-jual-rumah-depok-lokasi-strategis-asri-dan-dekat.html              
    350     157   80       http://rumahdijual.com/depok/1179319-rumah-second-di-kalimulya-depok-sangat-strategis-harga-350-a.html    
    350     152   152      http://rumahdijual.com/depok/1206367-kontrakan-4-pintu-di-sindangkarsa-bhakti-abri-depok-cocok.html       
    350     143   112      http://rumahdijual.com/depok/254844-rumah-strategis-dekat-tol-cijago.html                                 
    350     140   120      http://rumahdijual.com/depok/901886-rumah-murah-lokasi-bagus-depok-mampang-sawangan.html                  
    350     137   100      http://rumahdijual.com/depok/1224994-rumah-asri-nan-sejuk-masuk-mobil.html                                
    350     128   56       http://rumahdijual.com/depok/1304848-rumah-minimalis-murah-di-depok.html                                  
    350     121   60       http://rumahdijual.com/depok/1300612-rumah-dalam-cluster-di-rangkapan-jaya-baru-harga-murah.html          
    350     120   54       http://rumahdijual.com/depok/890180-rumah-dikawasan-sejuk-cipayung-depok.html                             
    350     119   119      http://rumahdijual.com/depok/1165122-rumah-di-depok-margonda-belakang-margo-city.html                     
    350     110   110      http://rumahdijual.com/depok/649834-rumah-dijual-di-depok.html                                            
    350     108   50       http://rumahdijual.com/depok/907146-rumah-dijual-di-cinere-depok.html                                     
    350     107   60       http://rumahdijual.com/depok/1209906-rumah-siap-huni-lokasi-strategis-harga-nego.html                     
    350     106   86       http://rumahdijual.com/depok/967890-rumah-baru-direnovasi-di-ratu-jaya-depok.html                         
    350     106   70       http://rumahdijual.com/depok/1008979-jual-rumah-murah-di-depok-kota-tanah-106m-bangunan.html              
    350     104   60       http://rumahdijual.com/depok/1076092-rumah-ready-stock-di-citayam-cuma-1-unit.html                        
    350     101   101      http://rumahdijual.com/depok/919411-dijual-rumah-induk-kontrakan.html                                     
    350     100   90       http://rumahdijual.com/depok/1107023-rumah-masih-fresh-type-90-100-di-cilangkap-depok.html                
    350     100   90       http://rumahdijual.com/depok/1259952-rumah-batu-dan-kontrakan-1-pintu-dekat-jalan-raya.html               
    350     100   80       http://rumahdijual.com/depok/975858-rumah-dijual-lokasi-jatijajar.html                                    
    350     100   80       http://rumahdijual.com/depok/604259-rumah-asri-di-panmas-depok.html                                       
    350     100   100      http://rumahdijual.com/depok/1026050-di-jual-b-u-rumah-kontrakan-3-pintu-di.html                          
    352     84    50       http://rumahdijual.com/depok/1213417-wow-miliki-rumah-2-lantai-harga-350jt-dapat-3-a.html                 
    355     91    60       http://rumahdijual.com/depok/821016-rumah-baru-strategis-di-citayam-depok.html                            
    355     85    54       http://rumahdijual.com/depok/1211194-rumah-minimalis-siap-huni-di-depok.html                              
    355     84    47       http://rumahdijual.com/depok/519607-cluster-d-phaniisan-regency-terbaru-di-kalisuren-rumah-2-a.html       
    360     92    50       http://rumahdijual.com/depok/1097603-rumah-dekat-pusat-kota-depok.html                                    
    360     92    50       http://rumahdijual.com/depok/1090146-rumah-cluster-ready-siap-huni-depok.html                             
    360     90    80       http://rumahdijual.com/depok/863316-jual-rumah-dekat-kelurahan-meruyung-limo.html                         
    360     90    80       http://rumahdijual.com/depok/963331-rumah-murah-di-perumnas-depok-timur.html                              
    360     90    50       http://rumahdijual.com/depok/1020359-cluster-nyaman-harga-teman.html                                      
    360     84    50       http://rumahdijual.com/depok/1033700-rumah-murah-dan-nyaman-di-sawangan.html                              
    360     137   48       http://rumahdijual.com/depok/1136033-rumah-siap-huni-dijual-cepat-murah-asri-bebas-banjir.html            
    360     115   110      http://rumahdijual.com/depok/823076-beli-rumah-dapat-kompor-gas-2-tungku.html                             
    360     110   95       http://rumahdijual.com/depok/1078684-rumah-dahlia-mpg.html                                                
    360     110   85       http://rumahdijual.com/depok/633776-rumah-minimalis-di-sawangan.html                                      
    360     110   85       http://rumahdijual.com/depok/721894-rumah-nyaman-di-ratujaya-depok.html                                   
    360     108   80       http://rumahdijual.com/depok/1080426-jual-butuh-rumah-harga-360-jt-kawasan-depok.html                     
    360     100   50       http://rumahdijual.com/depok/529064-rumah-besar-harga-obral-dkt-stasiun-depok.html
    


```python
selectModerate(df, avg, unit)
```

    
    MODERATE PRICE
    -----------------
    is when the price is above average: 361 (million IDR) with above-average land: 80 (square meters) and above-average building: 46 (square meters)
    
    
    There are : 1582  items with above-average price and above-average land.
    
    There are : 355  items with above-average price, above-average land and above-average building.
    
    price  land building                                                                                                            url
    365     94    60       http://rumahdijual.com/depok/810987-rumah-cluster-depok-seken.html                                          
    365     94    50       http://rumahdijual.com/depok/1092538-rumah-cluster-depok-dekat-jalan-raya-dan-stasiun.html                  
    365     94    50       http://rumahdijual.com/depok/1089150-rumah-cluster-kota-depok-harga-paling-cucok.html                       
    365     92    50       http://rumahdijual.com/depok/1080521-rumah-cluster-siap-huni-murah-depok.html                               
    365     90    50       http://rumahdijual.com/depok/1024080-rumah-ready-stock-kota-depok.html                                      
    365     90    50       http://rumahdijual.com/depok/1034835-rumah-ready-stok-di-depok-harga-nya-pasti-cocok.html                   
    365     90    50       http://rumahdijual.com/depok/1127267-rumah-cantik-harga-unik-dan-menarik.html                               
    365     90    50       http://rumahdijual.com/depok/1076660-cluster-nyaman-harga-teman.html                                        
    365     80    55       http://rumahdijual.com/depok/1073485-rumah-cluster-one-gate-system-pitara-pancoran-mas-depok.html           
    365     80    55       http://rumahdijual.com/depok/1083963-beli-rumah-perlu-mikir-tapi-kelamaan-mikir-dapet-di.html               
    365     80    50       http://rumahdijual.com/depok/1027793-rumah-ready-stok-di-depok-harga-nya-pasti-cocok.html                   
    368     85    47       http://rumahdijual.com/depok/513543-pah-kapan-punya-rumah-2-lantai-mamah-pengen-punya.html                  
    368     85    47       http://rumahdijual.com/depok/781244-prsembahan-terbaik-utk-keluarga-anda-rumah-2-lantai-harga.html          
    369     80    54       http://rumahdijual.com/depok/1106130-rumah-baru-80-mtr-siap-huni-depok.html                                 
    369     111   90       http://rumahdijual.com/depok/298770-rumah-dijual-di-pasirputih-sawangan-depok.html                          
    370     96    50       http://rumahdijual.com/depok/1093082-rumah-cluster-no-tipu-tipu.html                                        
    370     92    50       http://rumahdijual.com/depok/1104174-iklan-rumah-cluster-sesuai-gambar.html                                 
    370     92    50       http://rumahdijual.com/depok/1069762-rumah-baru-sesuai-foto-100-asli-kota-depok.html                        
    370     91    60       http://rumahdijual.com/depok/1152981-rumah-siap-huni.html                                                   
    370     91    50       http://rumahdijual.com/depok/1073534-iklan-yang-lebih-murah-banyak-tapi-yang-asli-disini.html               
    370     90    50       http://rumahdijual.com/depok/1030496-rumah-minimalis-harga-termanis.html                                    
    370     90    50       http://rumahdijual.com/depok/1120291-rumah-nyaman-harga-teman.html                                          
    370     80    60       http://rumahdijual.com/depok/797575-rumah-baru-type-60-80-wadas-depok-lama.html                             
    370     80    54       http://rumahdijual.com/depok/1054101-rumah-siap-hunu-shm.html                                               
    370     80    54       http://rumahdijual.com/depok/1098347-rumah-kpr-380-dekat-angkot-maharaja-dtc-mall-depok.html                
    370     80    50       http://rumahdijual.com/depok/1134690-hunian-cluster-jalan-pitara-raya-kota-depok.html                       
    370     80    50       http://rumahdijual.com/depok/1134619-rumah-cluster-di-jalan-pitara-raya.html                                
    370     80    50       http://rumahdijual.com/depok/1127924-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html           
    370     80    50       http://rumahdijual.com/depok/1113088-hunian-cluster-one-gate-system-di-pitara-pancoran-mas.html             
    370     80    50       http://rumahdijual.com/depok/1113104-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html           
    370     80    50       http://rumahdijual.com/depok/1113101-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html           
    370     80    50       http://rumahdijual.com/depok/1113151-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html           
    370     80    50       http://rumahdijual.com/depok/1113261-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html           
    370     80    50       http://rumahdijual.com/depok/1113287-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html           
    370     80    50       http://rumahdijual.com/depok/1113540-hunian-hook-dekat-jalan-raya-di-pitara-pancoran-mas.html               
    370     80    50       http://rumahdijual.com/depok/1127937-rumah-cluster-jalan-pitara-pancoran-mas-depok.html                     
    370     80    50       http://rumahdijual.com/depok/1135159-hunian-cluster-pitara-pancoran-mas-kota-depok.html                     
    370     80    50       http://rumahdijual.com/depok/737849-rumah-cluster-modern-minimalis-pastinya-strategis-daerah-kota-depok.html
    370     80    50       http://rumahdijual.com/depok/926933-rumah-sistem-cluster.html                                               
    370     80    50       http://rumahdijual.com/depok/1177083-rumah-sudah-siap-huni.html                                             
    370     80    50       http://rumahdijual.com/depok/1114185-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html           
    370     80    50       http://rumahdijual.com/depok/1114140-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html           
    370     80    50       http://rumahdijual.com/depok/924530-rumah-cluster-kota-depok.html                                           
    370     80    50       http://rumahdijual.com/depok/1055004-rumah-cluster-di-pitara-depok.html                                     
    370     80    50       http://rumahdijual.com/depok/1055007-rumah-cluster-di-pitara-depok-terjangkau.html                          
    370     80    50       http://rumahdijual.com/depok/927737-rumah-depok.html                                                        
    370     80    50       http://rumahdijual.com/depok/1135172-perumahan-cluster-griya-pratama-asri.html                              
    370     160   100      http://rumahdijual.com/depok/997368-rumah-besar-siap-huni-lt-1600-meter-lb-100-a.html                       
    370     150   80       http://rumahdijual.com/depok/1288014-rumah-di-sukatani-depok.html                                           
    370     125   60       http://rumahdijual.com/depok/867290-rumah-kalimulya-depok.html                                              
    370     104   60       http://rumahdijual.com/depok/817627-rumah-baru-siap-huni-lokasi-strategis-di-depok.html                     
    370     104   60       http://rumahdijual.com/depok/1079607-rumah-luas-tanah-104-depok-cipayung-ready-stock.html                   
    370     100   60       http://rumahdijual.com/depok/520068-rumah-cantik-depok.html                                                 
    370     100   60       http://rumahdijual.com/depok/1273411-di-jual-rumah-siap-huni-lokasi-stategis-di-cilodong.html               
    370     100   150      http://rumahdijual.com/depok/876247-jual-rumah-tingkat-di-jl-mangga-pasir-putih-sawangan.html               
    375     98    90       http://rumahdijual.com/depok/1070067-rumah-murah-strategis-di-depok-cluster-cagar-alam.html                 
    375     96    50       http://rumahdijual.com/depok/1095065-rumah-minimalis-terlaris-kota-depok.html                               
    375     96    50       http://rumahdijual.com/depok/1040105-rumah-idaman-keluarga-anda.html                                        
    375     96    50       http://rumahdijual.com/depok/1064197-masih-percaya-sama-iklan-tipuan.html                                   
    375     96    50       http://rumahdijual.com/depok/1064180-rumah-cluster-depok-ga-bikin-kapok-sekali-lihat-pasti.html             
    375     96    50       http://rumahdijual.com/depok/1064471-belanja-puas-harga-pass.html                                           
    375     96    50       http://rumahdijual.com/depok/1093014-rumah-cluster-bebas-biaya-surat-surat.html                             
    375     96    50       http://rumahdijual.com/depok/1058622-rumah-dekat-pusat-kota-depok.html                                      
    375     96    50       http://rumahdijual.com/depok/960186-rumah-cluster-mewah-harga-bersahabat.html                               
    375     95    50       http://rumahdijual.com/depok/1055888-rumah-minimalis-di-pancoran-mas.html                                   
    375     94    50       http://rumahdijual.com/depok/861720-rumah-cluster-mewah-harga-di-bawah-pasaran.html                         
    375     94    50       http://rumahdijual.com/depok/1075846-rumah-cluster-kota-depok-ready-stock-harga-pasti-cocok.html            
    375     93    52       http://rumahdijual.com/depok/952944-green-vallent-hill-citayam-hunian-asri-nyaman-dan-strategis.html        
    375     93    50       http://rumahdijual.com/depok/1052004-cluster-mewah-harga-murah.html                                         
    375     93    50       http://rumahdijual.com/depok/1072985-rumah-cluster-kota-depok-dekat-stasiun-dan-jalan-raya.html             
    375     92    50       http://rumahdijual.com/depok/1085823-rumah-mewah-dekat-stasiun.html                                         
    375     92    50       http://rumahdijual.com/depok/1085813-rumahnya-murah-lokasinya-bagus.html                                    
    375     92    50       http://rumahdijual.com/depok/1088584-rumah-minimalis-kota-depok.html                                        
    375     92    50       http://rumahdijual.com/depok/1077274-rumah-cluster-cipayung-depok.html                                      
    375     92    50       http://rumahdijual.com/depok/1079694-rumah-cantik-kualitas-oke-banget.html                                  
    375     92    50       http://rumahdijual.com/depok/1079862-rumah-cluster-idaman-keluarga.html                                     
    375     92    50       http://rumahdijual.com/depok/1101286-rumah-dan-harga-asli-tidak-menipu.html                                 
    375     92    50       http://rumahdijual.com/depok/1043406-cluster-luas-harga-puas.html                                           
    375     92    50       http://rumahdijual.com/depok/1043407-cluster-siap-huni-depok.html                                           
    375     92    50       http://rumahdijual.com/depok/1071208-rumah-baru-harga-lama.html                                             
    375     91    50       http://rumahdijual.com/depok/1061572-beli-rumah-di-sini-aja-dijamin-gak-bakalan-galau.html                  
    375     90    90       http://rumahdijual.com/depok/1232223-rumah-sukatani.html                                                    
    375     90    50       http://rumahdijual.com/depok/1101368-rumah-siap-huni-kota-depok.html                                        
    375     90    50       http://rumahdijual.com/depok/1035020-cari-rumah-yang-ready-aja-gak-pake-nunggu2-pembangunan.html            
    375     90    50       http://rumahdijual.com/depok/1058840-cari-yg-murah-yg-ga-ribet-pembayaran-nya-disini.html                   
    375     88    50       http://rumahdijual.com/depok/1302421-villa-pertiwi-strategis-dekat-terminal-depok-jatijajar.html            
    375     88    46       http://rumahdijual.com/depok/1284472-rumah-cluster-baru-di-depok.html                                       
    375     85    70       http://rumahdijual.com/depok/837652-dijual-rumah-murah-di-grogol-depok.html                                 
    375     80    70       http://rumahdijual.com/depok/1101563-rumah-cluster-pitara-kota-depok.html                                   
    375     80    55       http://rumahdijual.com/depok/1052297-cluster-murah-pitara.html                                              
    375     80    55       http://rumahdijual.com/depok/1128280-rumah-berbagai-macam-type-cluster.html                                 
    375     80    55       http://rumahdijual.com/depok/1055989-rumah-cluster-di-pitara-kota-depok.html                                
    375     80    55       http://rumahdijual.com/depok/1052274-rumah-murah-depok.html                                                 
    375     80    55       http://rumahdijual.com/depok/1125656-rumah-di-lokasi-yg-wwwwaahh.html                                       
    375     80    55       http://rumahdijual.com/depok/1097207-rumah-cluster-pitara.html                                              
    375     80    55       http://rumahdijual.com/depok/1104659-rumah-baru-cluster-55-80-a.html                                        
    375     80    55       http://rumahdijual.com/depok/1125658-rumah-di-lokasi-yg-wwwwaahh.html                                       
    375     80    55       http://rumahdijual.com/depok/1061989-rumah-oke-harga-oke-depok.html                                         
    375     80    55       http://rumahdijual.com/depok/1062651-rumah-di-depok-pitara.html                                             
    375     80    55       http://rumahdijual.com/depok/1063725-rumah-di-depok-pitara.html                                             
    375     80    55       http://rumahdijual.com/depok/1055960-rumah-ready-selangkah-ke-jalur-angkot.html                             
    375     80    55       http://rumahdijual.com/depok/1126693-rumah-manis-cluster-depok.html                                         
    375     80    55       http://rumahdijual.com/depok/1126690-rumah-cluster-banyak-type.html                                         
    375     80    55       http://rumahdijual.com/depok/1083740-rumah-hunian-cluster-pitara-pancoran-mas-one-gate-system.html          
    375     80    55       http://rumahdijual.com/depok/1072875-rumah-baru-harga-seru-pitara-depok.html                                
    375     80    55       http://rumahdijual.com/depok/1072864-pitara-cluster-depok-bebas-biaya-surat-dll.html                        
    375     80    55       http://rumahdijual.com/depok/1101395-rumah-cluster-di-pitara-kota-depok-strategis.html                      
    375     80    55       http://rumahdijual.com/depok/1101110-hunian-cluster-di-pitara-depok.html                                    
    375     80    55       http://rumahdijual.com/depok/1175013-rumah-cluster-15-mnt-ke-stasiun.html                                   
    375     80    55       http://rumahdijual.com/depok/1177777-rumah-cluster-lokasi-strategis.html                                    
    375     80    55       http://rumahdijual.com/depok/1101543-rumah-cluster-pitara-kota-depok.html                                   
    375     80    55       http://rumahdijual.com/depok/1101540-rumah-oke-harga-oke-depok.html                                         
    375     80    55       http://rumahdijual.com/depok/1101560-rumah-cluster-di-pitara-kota-depok-strategis.html                      
    375     80    55       http://rumahdijual.com/depok/1104660-rumah-baru-cluster-55-80-a.html                                        
    375     80    55       http://rumahdijual.com/depok/1104655-rumah-pitara-pancoran-mas-depok.html                                   
    375     80    55       http://rumahdijual.com/depok/1102316-rumah-baru-harga-murah-depok-pitara.html                               
    375     80    55       http://rumahdijual.com/depok/1106647-rumah-cluster-harga-ga-bikin-gemeter.html                              
    375     80    55       http://rumahdijual.com/depok/1101547-rumah-di-depok-pitara.html                                             
    375     80    55       http://rumahdijual.com/depok/1101390-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html            
    375     80    55       http://rumahdijual.com/depok/1101277-hunian-cluster-sangat-strategis-di-pitara-depok.html                   
    375     80    55       http://rumahdijual.com/depok/1101576-rumah-cluster-pitara-depok.html                                        
    375     80    55       http://rumahdijual.com/depok/1102723-rumah-kemana-mana-deket-kota-depok.html                                
    375     80    55       http://rumahdijual.com/depok/1114041-cluster-manis-pitara-depok.html                                        
    375     80    55       http://rumahdijual.com/depok/1087490-rumah-baru-harga-seru-depok.html                                       
    375     80    55       http://rumahdijual.com/depok/1072885-rumah-kota-harga-desa-pitara-kota-depok-strategis.html                 
    375     80    55       http://rumahdijual.com/depok/1125655-rumah-di-lokasi-yg-wwwwaahh.html                                       
    375     80    55       http://rumahdijual.com/depok/1062992-rumah-harga-murah-depok.html                                           
    375     80    55       http://rumahdijual.com/depok/1058799-tersisa-satu-unit-di-pitara-kota-depok.html                            
    375     80    55       http://rumahdijual.com/depok/1114416-rumah-cluster-harga-nego-pitara-depok.html                             
    375     80    55       http://rumahdijual.com/depok/1114053-cluster-griya-prarama-asri-pitara-depok.html                           
    375     80    55       http://rumahdijual.com/depok/1092268-rumah-cluster-lantai-full-granit.html                                  
    375     80    55       http://rumahdijual.com/depok/1221113-rumah-cluster-depok-pitara-raya.html                                   
    375     80    50       http://rumahdijual.com/depok/1181502-rumah-berkonsep-modern-dalam-cluster.html                              
    375     80    50       http://rumahdijual.com/depok/1098045-rumah-cluster-grya-pratama-asri-pitara-kota-depok.html                 
    375     80    50       http://rumahdijual.com/depok/1063669-rumah-murah-tapi-ga-murahan-pitara-depok.html                          
    375     80    50       http://rumahdijual.com/depok/893162-rumah-baru-kokoh-dan-bernilai.html                                      
    375     80    50       http://rumahdijual.com/depok/1209396-rumah-oke-harga-oke-depok.html                                         
    375     80    50       http://rumahdijual.com/depok/1209399-rumah-cluster-bebas-biaya-surat.html                                   
    375     80    50       http://rumahdijual.com/depok/1136467-rumah-cluster-banyak-type.html                                         
    375     80    50       http://rumahdijual.com/depok/1230851-rumah-cluster-mutiara-taman-jaya-depok.html                            
    375     80    50       http://rumahdijual.com/depok/1230339-rumah-cluster-mutiara-taman-jaya-depok.html                            
    375     80    50       http://rumahdijual.com/depok/1230357-cluster-mutiara-taman-jaya-depok.html                                  
    375     80    50       http://rumahdijual.com/depok/1143878-rumah-mewah-harga-murah-di-pitara-depok.html                           
    375     80    50       http://rumahdijual.com/depok/1103210-rumah-bebas-banjir-dan-anti-galau.html                                 
    375     80    50       http://rumahdijual.com/depok/1104883-hunian-cluster-jalan-pitara-raya.html                                  
    375     80    50       http://rumahdijual.com/depok/1230848-cluster-mutiara-taman-jaya-depok.html                                  
    375     80    50       http://rumahdijual.com/depok/1089313-rumah-murah-bagus-strategis-dan-aman-di-jalan-pitara.html              
    375     80    50       http://rumahdijual.com/depok/1108767-hunian-cluster-di-pitara-kota-depok-lantai-full-granite.html           
    375     80    50       http://rumahdijual.com/depok/1108545-hunian-cluster-di-pitara-kota-depok-lantai-full-granit.html            
    375     80    50       http://rumahdijual.com/depok/1108552-hunian-cluster-di-pitara-kota-depok-lantai-full-granit.html            
    375     80    50       http://rumahdijual.com/depok/1108761-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html            
    375     80    50       http://rumahdijual.com/depok/1108509-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html            
    375     80    50       http://rumahdijual.com/depok/1108776-rumah-cluster-pitara-pancoran-mas-kota-depok.html                      
    375     80    50       http://rumahdijual.com/depok/1058788-rumah-di-depok-pitara.html                                             
    375     80    50       http://rumahdijual.com/depok/1084120-rumah-cluster-pitara-depok.html                                        
    375     80    50       http://rumahdijual.com/depok/1181464-rumah-cluster-kota-depok.html                                          
    375     80    50       http://rumahdijual.com/depok/1184009-cluster-pitara-grya-pratama-asrin-kota-depok.html                      
    375     80    50       http://rumahdijual.com/depok/1233122-rumah-bebas-biaya-sertifikat.html                                      
    375     80    50       http://rumahdijual.com/depok/1058781-rumah-cluster-strategis-di-pitara-depok.html                           
    375     80    50       http://rumahdijual.com/depok/1097342-cluster-modern.html                                                    
    375     80    50       http://rumahdijual.com/depok/1182323-rumah-kota-depok.html                                                  
    375     80    50       http://rumahdijual.com/depok/1180520-rumah-cluster-kota-depok-pitara.html                                   
    375     80    50       http://rumahdijual.com/depok/1293760-ready-stok-cipayung-depok.html                                         
    375     80    50       http://rumahdijual.com/depok/995443-rumah-cluster-depok-dekat-stasiun.html                                  
    375     80    50       http://rumahdijual.com/depok/1056778-rumah-di-depok-pitara.html                                             
    375     80    50       http://rumahdijual.com/depok/1014462-jangan-lewatkan-kesempatan-emas-ini-beli-sekarang.html                 
    375     80    50       http://rumahdijual.com/depok/925715-murah-kokoh-kemana-mana-deket.html                                      
    375     80    50       http://rumahdijual.com/depok/1062050-rumah-cluster-50-90-harga-spesial-murah.html                           
    375     80    50       http://rumahdijual.com/depok/1113458-tersisa-satu-unit-di-pitara-depok.html                                 
    375     80    49       http://rumahdijual.com/depok/1120235-casa-perdana-3-a.html                                                  
    375     164   95       http://rumahdijual.com/depok/863173-rumah-murah-cipayung-depok.html                                         
    375     160   150      http://rumahdijual.com/depok/1271783-jual-cepat-rumah.html                                                  
    375     125   150      http://rumahdijual.com/depok/986633-rumah-impian-keluarga-2-lantai-jual-butuh.html                          
    375     125   144      http://rumahdijual.com/depok/1068161-rumah-dipasir-putih-depok.html                                         
    375     125   100      http://rumahdijual.com/depok/1177994-rumah-cluster-grya-pratama-asri-kota-depok.html                        
    375     112   65       http://rumahdijual.com/depok/818875-rumah-cluster-harga-terjangkau-depok.html                               
    375     112   60       http://rumahdijual.com/depok/809824-rumah-kpr-murah-depok.html                                              
    375     105   60       http://rumahdijual.com/depok/868598-hunian-nyaman-lokasi-strategis-di-citayam-1km-dari-stasiun.html         
    375     105   105      http://rumahdijual.com/depok/1195313-rumah-strategis-di-beji-depok.html                                     
    375     100   70       http://rumahdijual.com/depok/1314375-rumah-pasti-fotonya-asli-di-pitara-pancoran-mas-depok.html             
    375     100   70       http://rumahdijual.com/depok/1314399-rumah-baru-murah-jual-cepat-di-pitara-depok.html                       
    375     100   70       http://rumahdijual.com/depok/1314532-rumah-baru-murah-jual-cepat-di-pitara-depok.html                       
    375     100   70       http://rumahdijual.com/depok/1314542-rumah-baru-murah-jual-cepat-di-pitara-depok.html                       
    375     100   70       http://rumahdijual.com/depok/1314610-rumah-baru-murah-jual-cepat-di-pitara-depok.html                       
    375     100   70       http://rumahdijual.com/depok/1314758-rumah-baru-murah-jual-cepat-di-pitara-depok.html                       
    375     100   70       http://rumahdijual.com/depok/1315431-rumah-pasti-fotonya-asli-di-pitara-pancoran-mas-depok.html             
    375     100   70       http://rumahdijual.com/depok/1315662-rumah-pasti-di-pitara-pancoran-mas-depok.html                          
    375     100   70       http://rumahdijual.com/depok/1314362-rumah-baru-murah-jual-cepat-di-pitara-depok.html                       
    375     100   70       http://rumahdijual.com/depok/1314344-rumah-baru-murah-jual-cepat-di-pitara-depok.html                       
    375     100   100      http://rumahdijual.com/depok/1165526-dijual-rumah-petakan-2-pintu-sawangan-depok.html                       
    375     100   100      http://rumahdijual.com/depok/823743-rumah-100-meter-100-meter-ke-angkot-depok-lama.html                     
    378     110   90       http://rumahdijual.com/depok/1019328-rumah-second-jl-remaja.html                                            
    380     96    50       http://rumahdijual.com/depok/853619-rumah-murah-di-depok.html                                               
    380     92    50       http://rumahdijual.com/depok/1037781-rumah-cluster-selangkah-ke-jalur-angkot.html                           
    380     91    50       http://rumahdijual.com/depok/1003364-rumah-baru-di-gg-duren-parung-bingung-pancoran-mas.html                
    380     90    90       http://rumahdijual.com/depok/1254501-rumah-di-sukatani.html                                                 
    380     90    80       http://rumahdijual.com/depok/1047969-rumah-nyaman-di-depok-2-timur-dekat-stasiun-depok.html                 
    380     90    70       http://rumahdijual.com/depok/1304056-di-jual-rumah-asri-cakep-siap-huni-di-cipayung.html                    
    380     88    60       http://rumahdijual.com/depok/1018818-rumah-siap-huni-di-kali-baru-cilodong-depok-perumahan.html             
    380     86    50       http://rumahdijual.com/depok/1147901-rumah-baru-di-tapos-depok-unfurnished-murah-bebas-banjir.html          
    380     80    55       http://rumahdijual.com/depok/1033515-cluster-di-kota-depok.html                                             
    380     80    54       http://rumahdijual.com/depok/1253758-cluster-villa-sawangan-depok.html                                      
    380     150   140      http://rumahdijual.com/depok/963159-kontrakan-5-pintu-murah-di-depok-cibinong.html                          
    380     128   69       http://rumahdijual.com/depok/1271233-over-credit-rumah-mewah-di-akasia-terrace-pondok-petir.html            
    380     120   58       http://rumahdijual.com/depok/977759-perumahan-murah-fasilitas-lengkap-sawangan-depok.html                   
    380     110   80       http://rumahdijual.com/depok/221195-jual-rumah-seken-di-kampung-bulak-cinangka-sawangan-depok.html          
    380     110   100      http://rumahdijual.com/depok/1138297-rumah-di-jual-di-bulak-timur.html                                      
    380     109   96       http://rumahdijual.com/depok/1008384-rumah-di-jual-rumah-baru-siap-huni-lokasi-strategis.html               
    380     102   120      http://rumahdijual.com/depok/1296613-11-di-jual-rumah-ada-kios-pinggir-jalan-perumnas.html                  
    380     100   70       http://rumahdijual.com/depok/1138945-rumah-mewah-harga-ekonomis-di-kavling-rangkapan-jaya.html              
    385     96    65       http://rumahdijual.com/depok/944117-hunian-asri-berkualitas-dan-terjangkau-daerah-depok.html                
    385     90    70       http://rumahdijual.com/depok/1124203-rumah-murah-masuk-mobil-di-jl-keresek-tanah-baru.html                  
    385     85    60       http://rumahdijual.com/depok/651684-rumah-cluster-3-kamar-tidur.html                                        
    385     85    60       http://rumahdijual.com/depok/651721-rumah-cluster-3-kamar-tidur.html                                        
    385     85    50       http://rumahdijual.com/depok/1211176-rumah-minimalis-berkualitas.html                                       
    385     85    50       http://rumahdijual.com/depok/1233115-rumah-cluster-cantik-kualitas-baik-harga-menarik.html                  
    385     85    50       http://rumahdijual.com/depok/1213313-rumah-siap-huni-di-depok.html                                          
    385     84    60       http://rumahdijual.com/depok/1011347-dijual-1-unit-rumah-graha-khairina-bedahan-sawangan-depok.html         
    385     84    48       http://rumahdijual.com/depok/669538-perumahan-shaffa-residence-cibinong-kpr-tanpa-dp-dekat-stasiun.html     
    385     80    60       http://rumahdijual.com/depok/1065255-cluster-bebas-banjir-di-kota-depok.html                                
    385     80    55       http://rumahdijual.com/depok/1178421-nyari-rumah-kesana-kesini-blm-dapet-juga-murah-berkualitas.html        
    385     80    55       http://rumahdijual.com/depok/1222535-beli-rumah-dapat-mobil.html                                            
    385     80    55       http://rumahdijual.com/depok/1061477-beli-rumah-dekat-dengan-dtc-maharaja-pusat-perbelanjaan-disini.html    
    385     80    55       http://rumahdijual.com/depok/1063939-rumah-depok-minimalis-masuk-2-mobil-strategis.html                     
    385     80    55       http://rumahdijual.com/depok/1058655-rumah-80-meter-lantai-granite-dipitara.html                            
    385     80    55       http://rumahdijual.com/depok/1061521-ayo-ayo-beli-rumah-di-depok-investasi-menguntungkan-dan.html           
    385     80    55       http://rumahdijual.com/depok/1060676-rumah-ready-stock-1-lantai-full-granite-posisi-hook.html               
    385     80    50       http://rumahdijual.com/depok/926726-cluster-ruby.html                                                       
    385     80    50       http://rumahdijual.com/depok/1245901-rumah-bali-style-dgn-lebar-muka-7m2.html                               
    385     139   100      http://rumahdijual.com/depok/911552-rumah-dijual-murah-di-depok-murah-dan-strategis.html                    
    385     111   98       http://rumahdijual.com/depok/1189502-dijual-rumah-murah-dan-nyaman-di-sawangan-depok.html                   
    385     102   50       http://rumahdijual.com/depok/889698-rumah-murah-di-sawangan-depok.html                                      
    385     100   60       http://rumahdijual.com/depok/1273608-rumah-murah-n-strategis-pondok-terong-citayam-depok.html               
    387     82    55       http://rumahdijual.com/depok/1276312-rumah-kpr-3-kamar-tidur-5-menit-2km-ke.html                            
    387     231   80       http://rumahdijual.com/depok/974190-harga-bagus-rumah-besar-tanah-luas-depok.html                           
    390     90    50       http://rumahdijual.com/depok/962300-rumah-cluster-kota-depok.html                                           
    390     90    50       http://rumahdijual.com/depok/707151-rumah-murah-depok.html                                                  
    390     88    60       http://rumahdijual.com/depok/1019080-rumah-depok-gdc-lokasi-strategis.html                                  
    390     88    150      http://rumahdijual.com/depok/627605-rumah-baru-siap-huni-di-citayam.html                                    
    390     86    48       http://rumahdijual.com/depok/1068852-rumah-baru-86-meter-kpr-kalimulya.html                                 
    390     84    60       http://rumahdijual.com/depok/901407-rumah-baru-dijual-cepat.html                                            
    390     84    50       http://rumahdijual.com/depok/1118556-rumah-siap-huni-di-depok.html                                          
    390     84    46       http://rumahdijual.com/depok/912636-perumahan-q-naya-regency-pasir-putih-sawangan-depok.html                
    390     80    54       http://rumahdijual.com/depok/1191610-cluster-villa-sawangan-depok.html                                      
    390     80    50       http://rumahdijual.com/depok/704598-cluster-kalimulya-rumah-pantas-unit-terbatas.html                       
    390     80    48       http://rumahdijual.com/depok/962592-rumah-di-cipayung-depok-bisa-kpr-390jt.html                             
    390     110   100      http://rumahdijual.com/depok/1144460-dijual-rumah-di-beji-depok-110m-shm.html                               
    390     110   100      http://rumahdijual.com/depok/1170902-jual-cepat-rumah-strategis-di-depok.html                               
    390     100   98       http://rumahdijual.com/depok/1249613-rumah-shm-100m2-pasir-putih-di-jual-murah.html                         
    390     100   50       http://rumahdijual.com/depok/1060514-rumah-baru-selangkah-dr-stasiun.html                                   
    390     100   50       http://rumahdijual.com/depok/1089262-gratis-ac-toren-pagar-kanopi-stock-terbatas.html                       
    392     84    50       http://rumahdijual.com/depok/1124134-rumah-murah-siap-huni-d-depok.html                                     
    395     96    50       http://rumahdijual.com/depok/1002441-rumah-deket-stasiun-citayam-dan-depok-lama.html                        
    395     88    120      http://rumahdijual.com/depok/1027543-jual-rumah-bu-dibawah-pasaran.html                                     
    395     84    50       http://rumahdijual.com/depok/1116505-rumah-siap-huni-di-depok.html                                          
    395     84    50       http://rumahdijual.com/depok/1202663-rumah-murah-siap-huni-pancoran-mas-depok.html                          
    395     80    54       http://rumahdijual.com/depok/132101-rumah-murah-di-sawangan-depok.html                                      
    395     140   100      http://rumahdijual.com/depok/1256468-dijual-rumah-mewah-murah-1-bulan-lagi-finishing-140m.html              
    395     125   150      http://rumahdijual.com/depok/986628-rumah-lantai-murah.html                                                 
    395     104   50       http://rumahdijual.com/depok/878354-cluster-minimalis-permata-wadas-di-pitara-depok.html                    
    395     100   70       http://rumahdijual.com/depok/1001034-rumah-deket-grand-depok-city-15-mnt-ke-stasiun.html                    
    396     90    145      http://rumahdijual.com/depok/1043522-rumah-besar-bonus-kamar-kos-di-depok-timur-murah.html                  
    399     118   55       http://rumahdijual.com/depok/1300774-rumah-cantik-murah-luas-banyak-bonusnya.html                           
    399     110   100      http://rumahdijual.com/depok/1282643-rumah-dijual-cimanggis-depok.html                                      
    399     100   48       http://rumahdijual.com/depok/800163-tanpa-dp-dp-ringan-mini-townhouse-64-unit-sawangan.html                 
    400     99    80       http://rumahdijual.com/depok/776567-rumah-di-perumnas-depok-2-a.html                                        
    400     97    55       http://rumahdijual.com/depok/945460-rumah-minimalis-lokasi-pitara-depok.html                                
    400     96    60       http://rumahdijual.com/depok/785630-di-jual-rumah-strategis-di-wilayah-depok.html                           
    400     95    50       http://rumahdijual.com/depok/1081930-rumah-hook-di-pitara-depok.html                                        
    400     95    50       http://rumahdijual.com/depok/1093875-rumah-elit-harga-irit.html                                             
    400     95    50       http://rumahdijual.com/depok/1083661-rumah-elit-harga-irit.html                                             
    400     94    72       http://rumahdijual.com/depok/1209699-rumah-cluster-cantik-kualitas-baik-harga-menarik.html                  
    400     93    50       http://rumahdijual.com/depok/1127100-manis-murah-kualitas-dan-legalitas-terjamin-depok.html                 
    400     92    80       http://rumahdijual.com/depok/399403-rumah-dijual-komplek-tanah-baru.html                                    
    400     91    51       http://rumahdijual.com/depok/590869-rumah-dengan-lingkungan-yang-nyaman-dan-asri-di-kalibaru.html           
    400     90    80       http://rumahdijual.com/depok/1051720-perumnas-depok-timur.html                                              
    400     90    60       http://rumahdijual.com/depok/974927-rumah-cluster.html                                                      
    400     90    60       http://rumahdijual.com/depok/1069039-rumah-baru-asri-gede-3-kamar-siap-huni-di.html                         
    400     90    50       http://rumahdijual.com/depok/656405-cluster-madani-harga-pantas-unit-terbatas.html                          
    400     89    50       http://rumahdijual.com/depok/970377-dijual-rumah-perumnas.html                                              
    400     89    49       http://rumahdijual.com/depok/854382-di-jual-rumah-dp-murah-area-pancoranmas.html                            
    400     88    60       http://rumahdijual.com/depok/976531-sudah-baru-bagus-dan-murah-lagi-cepetan-deh.html                        
    400     88    60       http://rumahdijual.com/depok/1060101-rumah-siap-huni-di-kali-baru-cilodong-depok.html                       
    400     88    60       http://rumahdijual.com/depok/1017891-rumah-siap-huni-di-kali-baru-cilodong-depok.html                       
    400     87    50       http://rumahdijual.com/depok/886650-rumah-cluster-kota-depok.html                                           
    400     85    70       http://rumahdijual.com/depok/1162565-runah-second-siap-huni-ada-kios-nya-di-beji.html                       
    400     85    60       http://rumahdijual.com/depok/1012406-ruamh-second-minimalis-di-beji-murah.html                              
    400     85    55       http://rumahdijual.com/depok/794458-3-kamar-tidur-2-kamar-mandi-depok.html                                  
    400     85    50       http://rumahdijual.com/depok/839388-rumah-permata-wadas-depok-pitara.html                                   
    400     84    50       http://rumahdijual.com/depok/942116-rumah-murah-siap-huni-di-belakang-grand-depok-city.html                 
    400     84    48       http://rumahdijual.com/depok/1032573-jual-4-unit-rumah-baru-samping-perum-cinere-residence.html             
    400     83    48       http://rumahdijual.com/depok/877808-punya-rumah-di-kota-depok-atau-berinvestasi-lokasi-ini.html             
    400     82    50       http://rumahdijual.com/depok/1204919-rumah-murah-area-strategis-lokasi-payment-fleksibel.html               
    400     81    51       http://rumahdijual.com/depok/845159-rumah-murah-di-cinere-limo-depok.html                                   
    400     80    70       http://rumahdijual.com/depok/1115783-rumah-cluster-grya-pratama-asri-depok.html                             
    400     80    60       http://rumahdijual.com/depok/692816-rumah-baru-di-jl-tigaputra-meruyung-cinere.html                         
    400     80    60       http://rumahdijual.com/depok/1088761-rumah-minimalis.html                                                   
    400     80    60       http://rumahdijual.com/depok/779430-hunian-cantik-harga-asik-modelnya-menarik-dekat-stasiun-depok.html      
    400     80    56       http://rumahdijual.com/depok/937456-permata-ruby.html                                                       
    400     80    55       http://rumahdijual.com/depok/1298562-rumah-murah-sawangan-permai.html                                       
    400     80    55       http://rumahdijual.com/depok/1064341-rumah-murah-di-pitara-depok.html                                       
    400     80    54       http://rumahdijual.com/depok/1023463-cluster-depok-harga-gak-bikin-kapok.html                               
    400     80    54       http://rumahdijual.com/depok/1033599-rumah-besar-harga-kesasar.html                                         
    400     80    54       http://rumahdijual.com/depok/1299892-rumah-di-depok-sawangan.html                                           
    400     80    54       http://rumahdijual.com/depok/1301849-rumah-di-sawngan-arco-depok.html                                       
    400     80    54       http://rumahdijual.com/depok/1201393-vila-sawangan-asri.html                                                
    400     80    54       http://rumahdijual.com/depok/1186577-rumah-villa-bojong-sari-depok.html                                     
    400     80    50       http://rumahdijual.com/depok/1299934-rumah-di-depok-siap-huni-kpr-cash.html                                 
    400     80    50       http://rumahdijual.com/depok/1301565-rumah-di-kali-mulya-siap-untuk-di-huni.html                            
    400     80    50       http://rumahdijual.com/depok/1301875-rumah-di-nkali-mulya-depok-siap-huni.html                              
    400     80    50       http://rumahdijual.com/depok/1046336-rumah-cluster-di-jalan-pitara-raya-dekat-jalan-raya.html               
    400     80    50       http://rumahdijual.com/depok/1046803-rumah-cluster-pitara-depok.html                                        
    400     80    50       http://rumahdijual.com/depok/1038993-rumah-luas-murah-depok.html                                            
    400     80    50       http://rumahdijual.com/depok/1037225-rumah-cluster-sangat-dekat-jalan-raya-depok.html                       
    400     180   120      http://rumahdijual.com/depok/1254066-dijual-rumah-di-tapos-depok.html                                       
    400     170   170      http://rumahdijual.com/depok/1246382-rumah-lt-170-lb-170-di-dekat-setu-cilangkap.html                       
    400     164   95       http://rumahdijual.com/depok/863117-rumah-murah-cipayung-depok.html                                         
    400     164   95       http://rumahdijual.com/depok/1265200-rumah-murah-di-cipayung-depok.html                                     
    400     160   80       http://rumahdijual.com/depok/724422-cang-cing-ade-rumah-dijual-nih.html                                     
    400     150   70       http://rumahdijual.com/depok/724140-di-jual-rumah-tanah-cilodong-76-a.html                                  
    400     144   100      http://rumahdijual.com/depok/1139330-dijual-rumah-di-bojongsari.html                                        
    400     140   140      http://rumahdijual.com/depok/1118140-rumah-di-depok-2-tengah.html                                           
    400     139   100      http://rumahdijual.com/depok/923316-dijual-cepat-rumah-di-depok-ii.html                                     
    400     135   100      http://rumahdijual.com/depok/1098417-rumah-murah-dijual-di-gang-jambu-rt-rw-03-a.html                       
    400     125   60       http://rumahdijual.com/depok/1274322-rumah-cluster-permata-rubby-2-dekat-stasiun.html                       
    400     121   70       http://rumahdijual.com/depok/969446-hunian-asri-harga-terjangkau-di-depok.html                              
    400     119   150      http://rumahdijual.com/depok/1257539-di-jual-rumah-siap-huni-di-jalan-di-jalan.html                         
    400     118   90       http://rumahdijual.com/depok/1284009-rumah-3-kamar-tidur-garasi-2-mobil-depan-rsud.html                     
    400     118   57       http://rumahdijual.com/depok/999159-rumah-harga-murah-di-depok-jawa-barat.html                              
    400     112   55       http://rumahdijual.com/depok/978824-dijual-rumah-minimalis-open-style-concept.html                          
    400     110   72       http://rumahdijual.com/depok/1096688-hunian-baru-dan-minimalis-lokasi-strategis-di-depok.html               
    400     110   60       http://rumahdijual.com/depok/942674-rumah-murah-depok-lama.html                                             
    400     107   70       http://rumahdijual.com/depok/889672-dijual-rumah-1-lantai-di-jalan-keadilan-rawa-denok.html                 
    400     105   105      http://rumahdijual.com/depok/989178-rumah-jl-poin-mas.html                                                  
    400     103   70       http://rumahdijual.com/depok/1310140-rumah-baru-siap-huni-di-rangkapan-jaya-harga-murah.html                
    400     100   90       http://rumahdijual.com/depok/901812-kontrakan-murah.html                                                    
    400     100   70       http://rumahdijual.com/depok/1308676-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html                  
    400     100   70       http://rumahdijual.com/depok/1308575-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html                  
    400     100   70       http://rumahdijual.com/depok/1308736-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html                  
    400     100   70       http://rumahdijual.com/depok/1308760-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html                  
    400     100   70       http://rumahdijual.com/depok/1308553-rumah-pasti-sesuai-foto-di-pitara-depok.html                           
    400     100   70       http://rumahdijual.com/depok/1308842-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html                  
    400     100   70       http://rumahdijual.com/depok/1308877-rumah-pasti-fotonya-asli-di-pitara-pancoran-mas-depok.html             
    400     100   70       http://rumahdijual.com/depok/1315828-rumah-pasti-di-pitara-pancoran-mas-depok.html                          
    400     100   70       http://rumahdijual.com/depok/1308889-rumah-pasti-fotonya-asli-di-pitara-pancoran-mas-depok.html             
    400     100   70       http://rumahdijual.com/depok/1309256-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html                  
    400     100   70       http://rumahdijual.com/depok/1309113-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html                  
    400     100   70       http://rumahdijual.com/depok/1309001-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html                  
    400     100   70       http://rumahdijual.com/depok/1308918-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html                  
    400     100   70       http://rumahdijual.com/depok/1308943-rumah-pasti-fotonya-asli-di-pitara-pancoran-mas-depok.html             
    400     100   70       http://rumahdijual.com/depok/1309579-rumah-pasti-fotonya-asli-di-pitara-pancoran-mas-depok.html             
    400     100   50       http://rumahdijual.com/depok/1267376-permata-rubby-cash-bertahap.html                                       
    400     100   50       http://rumahdijual.com/depok/914277-rumah-bikin-sumringah.html                                              
    400     100   50       http://rumahdijual.com/depok/910814-rumah-murah-ga-murahan.html                                             
    400     100   50       http://rumahdijual.com/depok/1100339-pesona-perigi-sawangan-2-lantai-400-juta.html
    


```python
selectExpensive(df, avg, unit)
```

    
    EXPENSIVE PRICE
    -----------------
    is when the price is above average: 361 (million IDR) but you only get land below average: 80 (square meters) and building below average: 46 (square meters).
    
    
    
    There are : 333  items that matched the EXPENSIVE category.
    
    price land building                                                                                                            url
    364     30   35       http://rumahdijual.com/depok/1221033-cluster-termurah-tanpa-dp-didaerah-depok.html                          
    364     30   35       http://rumahdijual.com/depok/1212068-rumah-bagus-di-depok.html                                              
    365     75   45       http://rumahdijual.com/depok/1142868-cluster-ruby-hunian-asri-strategis.html                                
    365     75   40       http://rumahdijual.com/depok/989863-rumah-asri-dan-nyaman-nempel-grand-depok-city-10-a.html                 
    365     72   45       http://rumahdijual.com/depok/1236190-gak-beli-di-sini-nyesel-deh-pokok-nya.html                             
    365     72   45       http://rumahdijual.com/depok/1289183-rumah-baru-nempel-stasiun-depok.html                                   
    365     72   45       http://rumahdijual.com/depok/1116733-rumah-cluster-100m-dari-akses-angkot.html                              
    365     72   45       http://rumahdijual.com/depok/1295822-rumah-kpr-cukup-jalan-kaki-ke-stasiun-depok-lama.html                  
    365     72   45       http://rumahdijual.com/depok/1092263-rumah-cluster-pitara-depok-lokasi-dekat-stasiun.html                   
    365     72   45       http://rumahdijual.com/depok/1125738-stop-beli-rumah-yang-asal-bangun-beli-rumah-di.html                    
    365     72   45       http://rumahdijual.com/depok/1081580-rumah-cluster-griya-cipayung-asri.html                                 
    365     72   45       http://rumahdijual.com/depok/1085679-rumah-cluster-pitara-depok-lokasi-dekat-stasiun.html                   
    365     72   45       http://rumahdijual.com/depok/1118065-cluster-gregetan.html                                                  
    365     72   45       http://rumahdijual.com/depok/1087532-buruan-boking-sekarang-juga-jangan-di-tunda_tunda-unit-terbatas.html   
    365     72   45       http://rumahdijual.com/depok/1088062-beli-rumah-jangan-yang-asal-murah-ini-saya-kasih.html                  
    365     72   45       http://rumahdijual.com/depok/1085660-rumah-cluster-di-kota-harga-di-desa.html                               
    365     72   45       http://rumahdijual.com/depok/1111429-rumah-adem-bikin-tentrem.html                                          
    365     72   45       http://rumahdijual.com/depok/1250846-rumah-ready-baru-siap-huni-200m-ke-jlan-raya.html                      
    365     72   45       http://rumahdijual.com/depok/1086126-rumah-mewah-termurah-di-depok.html                                     
    365     72   45       http://rumahdijual.com/depok/1113517-kebanyakan-bulak-balik-pas-balik-harga-naik.html                       
    365     68   38       http://rumahdijual.com/depok/904372-cluster-nyaman-di-nuansa-maulia-cilodong-depok.html                     
    365     65   45       http://rumahdijual.com/depok/868205-rumah-hijau-di-cipayung-jaya-dekat-stasiun-citayam.html                 
    365     65   45       http://rumahdijual.com/depok/868223-rumah-hijau-di-cipayung-jaya-dekat-stasiun-citayam-kpr.html             
    367     72   36       http://rumahdijual.com/depok/1004993-cluster-dmawa-cinangka-hills-hunian-islami-berkonsep-syariah-murni.html
    367     65   30       http://rumahdijual.com/depok/1279111-rumah-dekat-tol-cijago-murah-300-jutaan-di-depok.html                  
    367     59   30       http://rumahdijual.com/depok/1257708-cluster-di-cimanggis-depok.html                                        
    368     72   40       http://rumahdijual.com/depok/1246311-rumah-cluster-300-jutaan-nempel-gdc-depok.html                         
    368     72   36       http://rumahdijual.com/depok/1040169-thegreenhill-depok-view-mempesona-dp-sukarela-tanpa-dp.html            
    368     60   30       http://rumahdijual.com/depok/1302553-perumahan-new-radiva-residence-di-cimanggis-depok.html                 
    368     60   30       http://rumahdijual.com/depok/1258937-rumah-manis-minimalis-di-cimanggis-depok-300-jutaan.html               
    369     75   40       http://rumahdijual.com/depok/1049281-sulambayang-hill-hanya-15-menit-dari-stasiun-depok-lama.html           
    369     72   43       http://rumahdijual.com/depok/917824-dapatkan-rumah-hanya-27-jt-di-angsur-6-kali.html                        
    369     72   40       http://rumahdijual.com/depok/1061483-rumah-depok-dekat-gdc.html                                             
    369     72   40       http://rumahdijual.com/depok/1249176-rumah-murah-300-jutaan-di-depok-i-10-menit.html                        
    369     72   40       http://rumahdijual.com/depok/1279084-rumah-murah-15-menit-ke-stasiun-cl-belakang-grand.html                 
    369     72   40       http://rumahdijual.com/depok/1276690-sulambayang-hill-dekat-stasiun-depok-lama-081225517642-a.html          
    369     72   40       http://rumahdijual.com/depok/1276747-cluster-modern-dan-mudah-terjangkau-di-depok-081225517642-a.html       
    369     72   40       http://rumahdijual.com/depok/1296114-sulambayang-hill-300jutaan-gdc-depok.html                              
    369     72   40       http://rumahdijual.com/depok/1296113-cluster-cantik-gdc-15-menit-stasiun-depok-lama.html                    
    369     72   40       http://rumahdijual.com/depok/1276723-hunian-nyaman-dan-murah-di-depok-081225517642-a.html                   
    369     72   40       http://rumahdijual.com/depok/1276717-berkonsep-modern-sulambayang-hill-depok-081225517642-a.html            
    369     72   40       http://rumahdijual.com/depok/1276514-di-pasarkan-rumah-dengan-desain-mewah-spek-wah-depok.html              
    369     72   40       http://rumahdijual.com/depok/1276703-depok-cluster-modern-harga-terjangkau-081225517642-a.html              
    369     60   45       http://rumahdijual.com/depok/894206-rumah-cantik-ekslusif-hanya-5-menit-dari-tol-depok.html                 
    370     75   40       http://rumahdijual.com/depok/1264343-rumah-cantik-harga-bersahabat-370-juta-di-depok.html                   
    370     75   38       http://rumahdijual.com/depok/1039726-perumahan-cipayung-paradiso.html                                       
    370     75   38       http://rumahdijual.com/depok/777993-jual-rumah-kpr-murah-di-cipayung-paradiso-dekat-stasiun.html            
    370     72   45       http://rumahdijual.com/depok/1314874-rumah-grand-putra-mandiri-kpr-dp-0-a.html                              
    370     72   45       http://rumahdijual.com/depok/1309747-rumah-baru-siap-huni-dekat-dengan-jalan-raya-200-a.html                
    370     72   45       http://rumahdijual.com/depok/1268100-cluster-djohar-sawangan-dp-suka-suka-bebas-biaya-apapun.html           
    370     72   45       http://rumahdijual.com/depok/1085043-rumah-baru-72-mtr-kpr-cipayung-depok.html                              
    370     72   45       http://rumahdijual.com/depok/1129258-perumahan-djohar-kpr-tanpa-dp-data-sulit-dibantu.html                  
    370     72   36       http://rumahdijual.com/depok/987180-rumah-dekat-pondok-cabe-termurah-hanya-300-jutaan.html                  
    370     72   30       http://rumahdijual.com/depok/1258108-cari-rumah-sederhana-type-30-72-radiva-residence-di.html               
    370     72   30       http://rumahdijual.com/depok/1019478-rumah-murah-di-permata-depok-regency.html                              
    370     66   45       http://rumahdijual.com/depok/1268269-rumah-siap-huni-dekat-dtc-depok.html                                   
    370     66   45       http://rumahdijual.com/depok/1008051-rumah-mungil-bisa-kpr-di-depok.html                                    
    370     64   45       http://rumahdijual.com/depok/1230796-launching-ratu-jaya-residence.html                                     
    370     60   45       http://rumahdijual.com/depok/484472-rumah-type-50-second-3thn-di-cluster-mampang-depok.html                 
    370     60   30       http://rumahdijual.com/depok/740685-rumah-murah-model-cluster-di-cimanggis-kota-depok.html                  
    371     72   36       http://rumahdijual.com/depok/1205391-cluster-ready-di-over-kredit-di-cluster-depok-r21.html                 
    372     77   45       http://rumahdijual.com/depok/620711-jual-rumah-kpr-dp-murah-di-perum-johar-jl.html                          
    372     60   30       http://rumahdijual.com/depok/1249905-hunian-murah-dekat-tol-cijago-cimanggis-radiva-residence-depok.html    
    372     60   30       http://rumahdijual.com/depok/1267739-cluster-murah-di-cimanggis-depok.html                                  
    373     65   36       http://rumahdijual.com/depok/1097959-rumah-cantik-dengan-harga-promosi-akhir-tahun-di-limo.html             
    375     78   45       http://rumahdijual.com/depok/1002463-rumah-sudah-ready-surat-udah-nongkrong.html                            
    375     76   44       http://rumahdijual.com/depok/519711-jual-rumah-di-jl-hj-midi-limo-depok.html                                
    375     75   45       http://rumahdijual.com/depok/838829-wismamas-pd-cabe-blok-c4-no-12-cinangka-sawangan.html                   
    375     75   45       http://rumahdijual.com/depok/1106182-sudah-dapat-belum-rumah-nya-sudah-mampir-kesini-belum.html             
    375     75   40       http://rumahdijual.com/depok/1311242-rumah-siap-huni.html                                                   
    375     75   38       http://rumahdijual.com/depok/906760-perumahan-cipayung-paradeso.html                                        
    375     75   38       http://rumahdijual.com/depok/1244309-rumah-375jt-di-limo-blk-kubah-mas.html                                 
    375     75   38       http://rumahdijual.com/depok/1248325-rumah-375juta-di-limo-depok-blkg-kubah-mas.html                        
    375     74   45       http://rumahdijual.com/depok/1124189-rumah-murah-sisa-2-unit-di-cipayung-depok-kpr.html                     
    375     74   42       http://rumahdijual.com/depok/1239270-rumah-baru-terbaik-di-meruyung-depok-dekat-margonda.html               
    375     72   45       http://rumahdijual.com/depok/1127057-rumah-ready-minimalis-konsep-depok.html                                
    375     72   45       http://rumahdijual.com/depok/1251478-rumah-cluster-pesona-anggrek-cipayung.html                             
    375     72   45       http://rumahdijual.com/depok/1035917-cluster-anggrek-depok.html                                             
    375     72   45       http://rumahdijual.com/depok/1071173-rumah-cluster-kota-depok.html                                          
    375     72   45       http://rumahdijual.com/depok/1177668-rumah-cluster-kota-depok-dekat-jalan-raya-dan-stasiun.html             
    375     72   45       http://rumahdijual.com/depok/1085952-rumah-murah-konsep-minimalis.html                                      
    375     72   45       http://rumahdijual.com/depok/1088906-rumah-minimalis-lokasi-nyaman.html                                     
    375     72   45       http://rumahdijual.com/depok/1222211-rumah-cluster-kota-depok.html                                          
    375     72   45       http://rumahdijual.com/depok/1081731-rumah-cluster-murah.html                                               
    375     72   45       http://rumahdijual.com/depok/1071299-iklan-rumah-cluster-ga-pake-bohong.html                                
    375     72   45       http://rumahdijual.com/depok/1089087-cluster-terlaris-di-depok.html                                         
    375     72   45       http://rumahdijual.com/depok/1226554-pesona-anggrek-sisa-1-unit-lagi.html                                   
    375     72   45       http://rumahdijual.com/depok/1226560-hunian-cluster-pesona-anggrek.html                                     
    375     72   45       http://rumahdijual.com/depok/1089171-hunian-cluster-bebas-banjir.html                                       
    375     72   45       http://rumahdijual.com/depok/1083964-rumah-elit-harga-irit.html                                             
    375     72   45       http://rumahdijual.com/depok/1071250-rumah-cluster-bebas-banjir-di-depok.html                               
    375     72   45       http://rumahdijual.com/depok/1220759-rumah-cluster-depok-dekat-jalan-raya.html                              
    375     72   45       http://rumahdijual.com/depok/961356-rumah-depok-minimalis-harga-murah-lokasi-strategis.html                 
    375     72   45       http://rumahdijual.com/depok/786798-ruamah-depok-pinggir-jalan-lok-citayam-harga-nego.html                  
    375     72   45       http://rumahdijual.com/depok/1040700-rumah-minimalis-depok-lokasi-strategis.html                            
    375     72   45       http://rumahdijual.com/depok/937602-perumahan-depok-sangat-murah-sekali.html                                
    375     72   45       http://rumahdijual.com/depok/1070023-rumah-hanya-selangkah-ke-jln-raya-cipayung-depok.html                  
    375     72   45       http://rumahdijual.com/depok/1206333-rumah-cluster-dekat-stasiun.html                                       
    375     72   45       http://rumahdijual.com/depok/1182350-rumah-tahap-finishing-dengan-gambar-tersebut.html                      
    375     72   45       http://rumahdijual.com/depok/1196365-rumah-kota-harga-desa.html                                             
    375     72   45       http://rumahdijual.com/depok/1203530-rumah-murah-di-depok.html                                              
    375     72   45       http://rumahdijual.com/depok/1124020-cluster-bikin-betah.html                                               
    375     72   45       http://rumahdijual.com/depok/1106190-cari-rumah-nih-saya-kasih-tips-nya.html                                
    375     72   45       http://rumahdijual.com/depok/1140471-depok-rumah-kpr-siap-huni-design-gaya-mewah.html                       
    375     72   45       http://rumahdijual.com/depok/979963-rumah-pinggir-jalan-ga-ribet-masuk-masuk-gang.html                      
    375     72   45       http://rumahdijual.com/depok/1125826-rumah-minimalis-lokasi-strategis-10-menit-dari-jl-margonda.html        
    375     72   45       http://rumahdijual.com/depok/1195867-stop-beli-rumah-yg-asal-bangun.html                                    
    375     72   45       http://rumahdijual.com/depok/1123612-rumah-strategis-idaman-keluarga.html                                   
    375     72   45       http://rumahdijual.com/depok/1240224-rumah-dep0k-kpr-dekat-dipo-kereta-siap-huni-design.html                
    375     72   45       http://rumahdijual.com/depok/1196990-rumah-kpr-siap-huni-gaya-mewah-di-cipayung-depok.html                  
    375     72   45       http://rumahdijual.com/depok/1040712-rumah-citayam-10-menit-dari-mall-cibinong.html                         
    375     72   45       http://rumahdijual.com/depok/961392-rumah-idaman-daerah-depok-lokasi-strategis-bebas-banjir.html            
    375     72   45       http://rumahdijual.com/depok/993372-rumah-citayam-city-15-menit-dari-depok.html                             
    375     72   45       http://rumahdijual.com/depok/1120246-cluster-dekat-stasiun-depok-lama.html                                  
    375     72   45       http://rumahdijual.com/depok/1040694-rumah-murah-lokasi-strategis-3-menit-dari-stasiun-kerata.html          
    375     72   45       http://rumahdijual.com/depok/1123564-rumah-depok-citayam-lokasi-strategis.html                              
    375     72   38       http://rumahdijual.com/depok/1289631-rumah-minimalis-cluster-deket-grand-depok-city-depok.html              
    375     72   36       http://rumahdijual.com/depok/900499-dijual-rumah-baru-type-36-72-di-pondok-petir.html                       
    375     72   36       http://rumahdijual.com/depok/1113772-rumah-minimalis.html                                                   
    375     72   30       http://rumahdijual.com/depok/1082386-rumah-nyaman-dan-asri-di-perumahan-mutiara-cimanggis-cilangkap.html    
    375     71   36       http://rumahdijual.com/depok/1272039-perumahan-samping-stasiun-depok-lama.html                              
    375     71   36       http://rumahdijual.com/depok/1244159-rumah-murah-nan-strategis-di-jl-raya-bogor.html                        
    375     70   45       http://rumahdijual.com/depok/997142-rumah-cluster-depok-dekat-jalan-raya-dan-stasiun.html                   
    375     70   45       http://rumahdijual.com/depok/1107668-rumah-dijual-di-parung-bingung-rangkapanjaya-baru-pancoran-mas.html    
    375     70   45       http://rumahdijual.com/depok/1254725-griya-artomoro-2-cilangkap-depok-rumah-aman-dan-nyaman.html            
    375     70   42       http://rumahdijual.com/depok/1315519-rumah-baru-terbaik-di-depok.html                                       
    375     70   42       http://rumahdijual.com/depok/1270816-rumah-di-limo-meruyung-dekat-kubah-mas-dekat-komplek.html              
    375     70   42       http://rumahdijual.com/depok/1226101-dijual-rumah-baru-paling-bagus-strategis-di-meruyung-depok.html        
    375     70   36       http://rumahdijual.com/depok/1104596-rumah-baru-bisa-kpr-banyak-untung-nya-dekat-mesjid.html                
    375     69   36       http://rumahdijual.com/depok/900680-perumahan-minimalis-puri-bella-depok.html                               
    375     68   45       http://rumahdijual.com/depok/1272063-rumah-siap-huni-diatas-maharaja-didepok.html                           
    375     66   36       http://rumahdijual.com/depok/1142209-perumahan-cluster-minimalis-galaksi-asri-2-kalimulya-depok.html        
    375     64   45       http://rumahdijual.com/depok/910126-di-cilodong-depok-strategis-minimalis-hanya-375-jutaan-free.html        
    375     62   32       http://rumahdijual.com/depok/1295529-kavling-di-jatijajar-depok-bogor-bni.html                              
    375     62   32       http://rumahdijual.com/depok/1031181-rumah-murah-di-jatijajar-depok.html                                    
    375     60   36       http://rumahdijual.com/depok/828673-rumah-murah-di-acropolis-cibinong-depok.html                            
    375     52   40       http://rumahdijual.com/depok/944243-rumah-murah-di-cinere-depok-cluster-santafi.html                        
    377     63   36       http://rumahdijual.com/depok/1104194-rumah-baru-griya-aditya-limo-depok.html                                
    378     72   43       http://rumahdijual.com/depok/997772-rumah-murah-di-depok-spek-premium-fasilitas-wahh.html                   
    378     60   36       http://rumahdijual.com/depok/1021638-cluster-griya-jajaten-depok.html                                       
    379     63   30       http://rumahdijual.com/depok/1258931-rumah-murah-minimalis-di-jatijajar-cimanggis-depok-300-jutaan.html     
    379     63   30       http://rumahdijual.com/depok/1302655-perumahan-jannar-residence-minimalis-manis-cimanggis-depok.html        
    380     76   36       http://rumahdijual.com/depok/574530-danu-residence-sawangan.html                                            
    380     74   40       http://rumahdijual.com/depok/1268568-rumah-murah-di-sawangan-dekat-depok-town-square-dtc.html               
    380     72   45       http://rumahdijual.com/depok/1040713-rumah-strategis-depok-citayam.html                                     
    380     72   45       http://rumahdijual.com/depok/1213250-rumah-cluster-kota-depok-sisa-1-unit.html                              
    380     72   45       http://rumahdijual.com/depok/1010012-rumah-minimalis-harga-terjangkau-di-lingkungan-yang-asri.html          
    380     72   42       http://rumahdijual.com/depok/1032104-jual-cepat-rumah-di-perumahan-alam-sukmajaya-depok.html                
    380     72   40       http://rumahdijual.com/depok/1140336-dijual-perumahan-di-pitara.html                                        
    380     72   38       http://rumahdijual.com/depok/1130717-perumahan-baru-cinangka-garden-hills-cinangka-yu.html                  
    380     72   38       http://rumahdijual.com/depok/924286-perumahan-griya-amanah-kalimulya-depok-belakang-gdc.html                
    380     72   38       http://rumahdijual.com/depok/1119729-dijual-rumah-baru-1-lantai-dalam-komplek-asri-dekat.html               
    380     72   36       http://rumahdijual.com/depok/593045-rumah-klaster-sawangan-depok.html                                       
    380     70   40       http://rumahdijual.com/depok/1272540-cluster-murah-di-bhakti-abri-pekapuran.html                            
    380     63   36       http://rumahdijual.com/depok/1101111-rumah-minimalis-cinere-limo.html                                       
    381     72   36       http://rumahdijual.com/depok/1210319-hunian-sejuk-di-selatan-jakarta.html                                   
    382     72   45       http://rumahdijual.com/depok/1272245-186-di-jual-rumah-cantik-asri-sejuk-permata-depok.html                 
    382     72   36       http://rumahdijual.com/depok/1112557-cluster-cantik-idaman-keluarga-harmonis.html                           
    382     72   30       http://rumahdijual.com/depok/1299703-rumah-cluster-dekat-bandara-pondok-cabe.html                           
    382     49   41       http://rumahdijual.com/depok/1213936-rumah-murah-di-cilodong-depok-siap-huni.html                           
    385     72   45       http://rumahdijual.com/depok/1133735-rumah-depok-daerah-cipayung-lokasi-strategis.html                      
    385     72   45       http://rumahdijual.com/depok/1135010-rumah-cipayung-200-m-dari-jalan-raya.html                              
    385     72   45       http://rumahdijual.com/depok/1134962-rumah-cipayung-20-menit-dari-jalan-tol-jagorawi.html                   
    385     72   45       http://rumahdijual.com/depok/1135005-rumah-depok-daerah-cipayung-lokasi-strategis.html                      
    385     72   45       http://rumahdijual.com/depok/958870-rumah-minimalis-depok-daerah-citayam-harga-nego.html                    
    385     72   45       http://rumahdijual.com/depok/1133591-rumah-siap-huni.html                                                   
    385     72   45       http://rumahdijual.com/depok/1133722-rumah-cipayung-idaman-lokasi-strategis-harga-nego.html                 
    385     72   45       http://rumahdijual.com/depok/1220485-rumah-cluster-depok-dekat-stasiun-dan-jalan-raya.html                  
    385     72   45       http://rumahdijual.com/depok/1133585-rumah-cipayung-idaman-lokasi-strategis-harga-nego.html                 
    385     72   45       http://rumahdijual.com/depok/1005598-rumah-minimalis-lokasi-strategis-dan-murah.html                        
    385     72   45       http://rumahdijual.com/depok/929012-rumah-type45-72-di-pramuka-raya-mampang-depok.html                      
    385     72   45       http://rumahdijual.com/depok/837730-rumah-cluster-harga-wafer.html                                          
    385     72   45       http://rumahdijual.com/depok/1005517-rumah-murah-lokasi-sangat-strategis.html                               
    385     72   45       http://rumahdijual.com/depok/1001856-rumah-murah-dan-lokasi-strategis.html                                  
    385     72   45       http://rumahdijual.com/depok/877063-rumah-cantik-depok-lokasi-strategis-3-menit-dari-stasiun.html           
    385     72   45       http://rumahdijual.com/depok/1001863-rumah-depok-citayam-lokasi-strategis-dan-murah.html                    
    385     72   45       http://rumahdijual.com/depok/941400-rumah-minimalis-depok-citayam-lok-sangat-strategis-harga-nego.html      
    385     72   40       http://rumahdijual.com/depok/761690-rumah-bagus-b-u-siap-huni-di-perumahan-dekat.html                       
    385     72   36       http://rumahdijual.com/depok/941747-dp-5jtan-sudah-free-surat2.html                                         
    385     72   36       http://rumahdijual.com/depok/926865-dp-5jtan-sudah-free-surat2.html                                         
    385     72   36       http://rumahdijual.com/depok/850843-rumah-depok-dp-10-a.html                                                
    385     70   40       http://rumahdijual.com/depok/1274964-rumah-cluster-di-grand-depok-city-murah-dp-rendah.html                 
    385     70   36       http://rumahdijual.com/depok/1238467-murah-rumah-baru-pondok-petir-depan-jalan-unit-terbatas.html           
    385     69   36       http://rumahdijual.com/depok/894855-rumah-minimalis-nan-anggun.html                                         
    385     60   40       http://rumahdijual.com/depok/910060-rumah-baru-minimalis-depok-15-mnt-ke-margonda-stasiun.html              
    386     65   30       http://rumahdijual.com/depok/1270987-cluster-dekat-tol-di-cimanggis-depok.html                              
    387     72   36       http://rumahdijual.com/depok/893285-mampang-depok-rumah-dengan-bayar-19-juta-langsung-proses.html           
    387     72   36       http://rumahdijual.com/depok/893297-mampang-depok-rumah-dengan-bayar-19-juta-langsung-proses.html           
    387     72   36       http://rumahdijual.com/depok/802261-dp-0-kpr-99-approve-jika-ambil-rumah-di.html                            
    387     72   36       http://rumahdijual.com/depok/812067-rumah-300-jutaan-dimampang-depok-kpr-pasti-disetujui.html               
    387     72   36       http://rumahdijual.com/depok/784496-tanpa-uang-muka-bisa-punya-rumah-di-depok.html                          
    387     72   36       http://rumahdijual.com/depok/893895-mampang-depok-rumah-dengan-bayar-19-juta-langsung-proses.html           
    387     72   36       http://rumahdijual.com/depok/890136-rumah-dp-ringan-akses-stasiun-depok-baru.html                           
    387     72   36       http://rumahdijual.com/depok/893310-mampang-depok-rumah-dengan-bayar-19-juta-langsung-proses.html           
    388     72   36       http://rumahdijual.com/depok/745583-rumah-depok-dekat-gdc-dan-stasiun-depok-lama.html                       
    389     72   36       http://rumahdijual.com/depok/741851-rumah-memukau-harga-terjangkau-di-kavling-indah-village.html            
    389     72   36       http://rumahdijual.com/depok/990652-banjaran-residence-kokoh-nyaman-dan-bebas-banjir-akses-pintu.html       
    390     78   36       http://rumahdijual.com/depok/741822-rumah-cantik-harga-menarik-kavling-pondok-petir.html                    
    390     72   45       http://rumahdijual.com/depok/1301349-dijual-rumah-harga-murah-kawasan-depok.html                            
    390     72   45       http://rumahdijual.com/depok/944697-rumah-berkonsep-syariah-tanpa-bank-tanpa-riba-di-depok.html             
    390     72   45       http://rumahdijual.com/depok/1036121-rosella-residence-rumah-cluster-dengan-harga-paling-murah-di.html      
    390     72   45       http://rumahdijual.com/depok/1048789-rumah-cluster-minimalis-rosella-residence-depok.html                   
    390     72   36       http://rumahdijual.com/depok/652216-rumah-cluster-baru-dan-bagus-di-kalimulya-depok.html                    
    390     70   40       http://rumahdijual.com/depok/902503-cluster-cantik-minimalis-dekat-pintu-tol-cijago.html                    
    390     62   36       http://rumahdijual.com/depok/1135738-rumah-dijual-di-limo-cinere-ddf.html                                   
    390     62   36       http://rumahdijual.com/depok/1138380-rumah-minimalis-di-cinere.html                                         
    390     62   32       http://rumahdijual.com/depok/1295218-angsuran-murah-dp-ringan-di-jatijajar-depok-bni.html                   
    391     65   36       http://rumahdijual.com/depok/1138630-rumah-murah-cinere-limo.html                                           
    391     63   36       http://rumahdijual.com/depok/1248495-dijual-rumah-murah-strategis-di-depok-dekat-jakarta-tangsel.html       
    391     62   36       http://rumahdijual.com/depok/1151001-rumah-dijual-di-depok-griya-aditya-cinere-lokasi-sangat.html           
    391     62   36       http://rumahdijual.com/depok/1135697-rumah-di-jual-di-cenere-depok.html                                     
    391     62   36       http://rumahdijual.com/depok/1292612-dijual-perumahan-griya-aditya-di-daerah-cinere.html                    
    391     62   36       http://rumahdijual.com/depok/1177630-gria-aditya-cinere-dekat-masjid-kubah-emas-depok.html                  
    391     62   36       http://rumahdijual.com/depok/1136014-jual-rumah-siap-huni-bonus-awal-tahun-menanti.html                     
    391     62   36       http://rumahdijual.com/depok/1196997-rumah-kpr-murah-di-cinere-dp-bisa-di-cicil.html                        
    391     62   36       http://rumahdijual.com/depok/1194933-rumah-cluster-baru-dan-siap-huni-di-limo-cinere.html                   
    391     62   36       http://rumahdijual.com/depok/1233416-rumah-dijual-di-limo-cinere-depok.html                                 
    391     62   36       http://rumahdijual.com/depok/1135919-jual-rumah-murah-dan-nyaman-di-depok.html                              
    391     62   36       http://rumahdijual.com/depok/1144061-rumah-murah-di-cinere-390jutaan-siapa-cepat-dia-dapat.html             
    391     62   36       http://rumahdijual.com/depok/1193305-dijual-rumah-di-cinere.html                                            
    391     62   36       http://rumahdijual.com/depok/1136718-rumah-murah-di-depok-griya-aditya-cinere-kota-depok.html               
    391     62   36       http://rumahdijual.com/depok/1233364-rumah-di-cinere-depok.html                                             
    391     62   36       http://rumahdijual.com/depok/1284684-rumah-murah-sejuk-dan-asri.html                                        
    392     73   42       http://rumahdijual.com/depok/328895-cluster-pandawa.html                                                    
    392     72   40       http://rumahdijual.com/depok/1167708-rumah-murah-sulambayang-hill-15-menit-dari-stasiun-depok.html          
    392     72   40       http://rumahdijual.com/depok/1204737-cluster-murah-15-menit-dari-sta-depok-lama.html                        
    392     72   40       http://rumahdijual.com/depok/1260799-rumah-baru-murah-di-kota-depok-sulambayang-hill-dekat.html             
    392     72   40       http://rumahdijual.com/depok/1178539-rumah-murah-dan-asri-di-cilodong-depok.html                            
    392     72   40       http://rumahdijual.com/depok/1204738-cluster-murah-15-menit-ke-stasiun-dpk-lama.html                        
    392     72   40       http://rumahdijual.com/depok/1171102-rumah-murah-15-menit-dr-sta-depok-lama.html                            
    392     72   40       http://rumahdijual.com/depok/1180813-rumah-cluster-di-cilodong-belakang-gdc-depok.html                      
    392     72   40       http://rumahdijual.com/depok/1194888-rumah-bagus-di-grend-depok-city-depok.html                             
    392     62   36       http://rumahdijual.com/depok/1183676-cluster-cantik-390jutaan-terbaik-dan-termurah-di-cinere.html           
    394     71   40       http://rumahdijual.com/depok/1179421-perumahan-radiva-tapos-depok.html                                      
    394     71   40       http://rumahdijual.com/depok/1174648-rumah-dijual-pekapuran-depok-bni.html                                  
    395     75   36       http://rumahdijual.com/depok/1030285-sawangan-gardenia-depok-rumah-cluster-dp-ringan-all-legalitas.html     
    395     75   36       http://rumahdijual.com/depok/1022667-sawangangardenia-mini-cluster-dp-murah-all-include-sertipikat-shm.html 
    395     72   45       http://rumahdijual.com/depok/1223989-rumah-cimanggis.html                                                   
    395     72   45       http://rumahdijual.com/depok/1309367-rumah-murah-dekat-gerbang-tol-cimanggis-depok.html                     
    395     72   45       http://rumahdijual.com/depok/1235545-dijual-rumah-akses-strategis-di-cimanggis-depok.html                   
    395     72   39       http://rumahdijual.com/depok/1280185-jual-rumah-grya-tanah-baru.html                                        
    395     72   39       http://rumahdijual.com/depok/1246542-dijual-beberapa-unit-rumah-tanah-baru-beji-depok.html                  
    395     72   39       http://rumahdijual.com/depok/1303894-di-jual-rumah-di-perbatasan-jakarta-depok.html                         
    395     72   38       http://rumahdijual.com/depok/898849-cluster-cantik-nuansa-maulia-jatimulya-depok-r21-0255-a.html            
    395     72   36       http://rumahdijual.com/depok/1029644-cluster-36-72-mtr-bisa-kpr-near-kalimulya.html                         
    395     72   36       http://rumahdijual.com/depok/741845-rumah-cantik-harga-menarik-di-kavling-athaya-grogol.html                
    395     70   42       http://rumahdijual.com/depok/1094219-rumah-baru-nuansa-modern-akses-dekat-mall-rumah-sakit.html             
    395     63   36       http://rumahdijual.com/depok/1140727-claster-griya-aditiya-cinere.html                                      
    395     63   36       http://rumahdijual.com/depok/1139289-rumah-murah-cantik-minimalis-di-cinere-depok.html                      
    395     63   36       http://rumahdijual.com/depok/1234535-cluster-dengan-harga-meriah-daerah-cinere-depok.html                   
    396     72   45       http://rumahdijual.com/depok/1173647-rumah-syariah-satu-lantai-cicil-tanpa-bunga-di-sawangan.html           
    397     72   36       http://rumahdijual.com/depok/1265711-masih-ada-kok-rumah-cicilan-3-5-juta-di.html                           
    397     72   36       http://rumahdijual.com/depok/1253611-rumah-siap-bangun-di-kelurahan-rangkapan-jaya-pancoran-mas.html        
    397     72   36       http://rumahdijual.com/depok/1247663-masih-ada-kok-rumah-cicilan-3-5-juta-di.html                           
    397     72   36       http://rumahdijual.com/depok/962835-mampang-depok-hanya-dengan-bayar-17jt-langsung-proses-kpr.html          
    397     72   36       http://rumahdijual.com/depok/1250025-rumah-siap-bangun-di-kelurahan-rangkapan-jaya-pancoran-mas.html        
    397     72   36       http://rumahdijual.com/depok/1258032-rumah-siap-bangun-di-kelurahan-rangkapan-jaya-pancoran-mas.html        
    397     72   36       http://rumahdijual.com/depok/1251848-rumah-siap-bangun-di-kelurahan-rangkapan-jaya-pancoran-mas.html        
    397     72   36       http://rumahdijual.com/depok/1276235-rumah-murah-di-depok-dijual-rumah-dalam-perumahan-di.html              
    397     72   36       http://rumahdijual.com/depok/1254279-rumah-di-rangkapan-jaya-depok-bayar-17-juta-langsung.html              
    397     72   35       http://rumahdijual.com/depok/1126275-rumah-hanya-300-juta-di-pinggir-jalan-raya-bogor.html                  
    398     72   36       http://rumahdijual.com/depok/1092457-rumah-baru-di-rangkapan-jaya-baru-dekat-arco-sawangan.html             
    398     70   40       http://rumahdijual.com/depok/1016579-dijual-rumah-manis-di-margonda-depok.html                              
    398     60   36       http://rumahdijual.com/depok/1143391-dijual-cluster-type-36-60-daerah-depok.html                            
    398     60   36       http://rumahdijual.com/depok/1121851-rumah-baru-tipe-36-60-kpr-rp-398jt-di.html                             
    398     60   36       http://rumahdijual.com/depok/1121881-rumah-baru-tipe-36-60-kpr-398jt-jl-raya.html                           
    398     60   36       http://rumahdijual.com/depok/1016312-kavling-raden-saleh-rumah-murah-bangunan-mewah.html                    
    399     36   38       http://rumahdijual.com/depok/1292076-perumahan-besar-poin-mas-total-500unit-lokasi-cinere-ujung.html        
    400     79   45       http://rumahdijual.com/depok/1146507-dijual-rumah-di-sawangan-permai-depok.html                             
    400     78   45       http://rumahdijual.com/depok/934785-town-house-88-cimanggis-dp-10jt-promo.html                              
    400     78   36       http://rumahdijual.com/depok/932253-rumah-di-pancoran-mas-mampang-depok.html                                
    400     76   45       http://rumahdijual.com/depok/1313794-perumahan-elok-fariasi.html                                            
    400     75   45       http://rumahdijual.com/depok/1205998-cluster-termurah-dp-suka-suka-hanya-di-daerah-depok.html               
    400     75   40       http://rumahdijual.com/depok/1196975-rumah-kpr-20-meter-ke-jalur-angkot-di-jl.html                          
    400     75   36       http://rumahdijual.com/depok/169369-pesona-grogol-2-depok-dekat-rencana-simpang-tol-antasari.html           
    400     74   45       http://rumahdijual.com/depok/1276902-rumah-depok-gdc.html                                                   
    400     74   38       http://rumahdijual.com/depok/1097555-rumah-murah-dan-strategis-di-kota-depok.html                           
    400     73   40       http://rumahdijual.com/depok/1276919-rumah-depok-cimanggis.html                                             
    400     72   45       http://rumahdijual.com/depok/1192195-rumah-daerah-depok-cipayung-lokasi-strategis.html                      
    400     72   45       http://rumahdijual.com/depok/1192188-rumah-minimalis-depok-citayam-lokasi-strategis.html                    
    400     72   45       http://rumahdijual.com/depok/1192185-rumah-minimalis-lokasi-strategis.html                                  
    400     72   45       http://rumahdijual.com/depok/1132099-rumah-depok-lokasi-strategis-bebas-banjir.html                         
    400     72   45       http://rumahdijual.com/depok/1132087-rumah-idaman-keluarga-lingkungan-asri-lokasi-strategis.html            
    400     72   45       http://rumahdijual.com/depok/1302420-jual-rumah-lokasi-strategis-dan-premium-di-dekat-gdc.html              
    400     72   45       http://rumahdijual.com/depok/1142615-rumah-depok-baru-dekat-stasiun.html                                    
    400     72   45       http://rumahdijual.com/depok/1093035-rumah-cluster-idaman-keluarga.html                                     
    400     72   45       http://rumahdijual.com/depok/362043-kavling-siap-bangun-4-unit-di-mampang-depok-type.html                   
    400     72   45       http://rumahdijual.com/depok/1019049-perumahan-di-depok-dengan-nuansa-alam-dan-modern.html                  
    400     72   45       http://rumahdijual.com/depok/1177155-rumah-lux-full-granite-posisi-hook.html                                
    400     72   45       http://rumahdijual.com/depok/1125838-rumah-minimalis-unit-terbatas-lokasi-strategis.html                    
    400     72   45       http://rumahdijual.com/depok/961337-rumah-minimalis-depok-daerah-citayam-lokasi-sangat-strategis-harga.html 
    400     72   45       http://rumahdijual.com/depok/936780-rumah-depok-minimalis-strategis-daerah-citayam.html                     
    400     72   45       http://rumahdijual.com/depok/1178522-rumah-cluster-nempel-jalan-raya-ga-ribet-masuk-gang.html               
    400     72   45       http://rumahdijual.com/depok/1069898-rumah-murah-di-grand-depok-city.html                                   
    400     72   45       http://rumahdijual.com/depok/1005528-rumah-idaman-lokasi-strategis-harga-nego.html                          
    400     72   45       http://rumahdijual.com/depok/1005581-rumah-cantik-depok-lokasi-strategis-harga-nego.html                    
    400     72   45       http://rumahdijual.com/depok/1252822-rumah-idaman-cipayung-jaya.html                                        
    400     72   45       http://rumahdijual.com/depok/1005544-rumah-depok-citayam-1-jam-dari-kota-bogor-lokasi.html                  
    400     72   38       http://rumahdijual.com/depok/1039325-rumah-desain-bali-modern-murah-kayana-residence-depok.html             
    400     72   38       http://rumahdijual.com/depok/1150817-rumah-cluster-termurah-dekat-gdc.html                                  
    400     72   36       http://rumahdijual.com/depok/734932-cluster-puri-khayangan-residence-kota-depok.html                        
    400     72   36       http://rumahdijual.com/depok/952992-rumah-di-permata-cimanggis-depok.html                                   
    400     72   30       http://rumahdijual.com/depok/444769-rumah-murah-mewah-strategis-300-jutaan-di-depok-permata.html            
    400     72   30       http://rumahdijual.com/depok/1304145-rumah-bagus-harga-murah.html                                           
    400     72   30       http://rumahdijual.com/depok/1304060-rumah-murah-siap-huni-di-selatan-depok.html                            
    400     72   30       http://rumahdijual.com/depok/466750-rumah-murah-minimalis-di-dalam-cluster-cantik-di-cimanggis.html         
    400     72   30       http://rumahdijual.com/depok/1311123-permata-cimanggis-rumah-idaman-keluarga-anda.html                      
    400     72   30       http://rumahdijual.com/depok/1297335-perumahan-murah-didepok.html                                           
    400     72   30       http://rumahdijual.com/depok/658260-permata-cimanggis-depok.html                                            
    400     72   30       http://rumahdijual.com/depok/967459-rumah-murah-konsep-cluster-jamrud-permata-cimanngis-depok.html          
    400     71   40       http://rumahdijual.com/depok/1221416-rumah-dijual-di-kalimulya-depok-dekat-gdc-pasar-dan.html               
    400     70   45       http://rumahdijual.com/depok/1316131-rumah-siap-huni-di-jatimulya.html                                      
    400     70   45       http://rumahdijual.com/depok/1316242-ready-stock-sisa-2-unit-di-jatimulya-cilodong-depok.html               
    400     70   45       http://rumahdijual.com/depok/1313028-rumah-baru-siap-huni-jatimulya-cilodong-depok.html                     
    400     70   45       http://rumahdijual.com/depok/1312977-rumah-baru-siap-huni-jatimulya-cilodong-depok.html                     
    400     70   45       http://rumahdijual.com/depok/1312997-rumah-ready-stock-2-unit-di-jatimulya-cilodong-depok.html              
    400     70   45       http://rumahdijual.com/depok/1313200-dijual-rumah-di-jatimulya-cilodong-depok.html                          
    400     70   45       http://rumahdijual.com/depok/1302909-brs-03-rumah-cluster-siap-huni-45-70-studio.html                       
    400     70   45       http://rumahdijual.com/depok/1314328-dijual-cepat-rumah-ready-stock-di-jatimulya-cilodong.html              
    400     70   45       http://rumahdijual.com/depok/1314699-rumah-ready-stock-di-cilodong-depok.html                               
    400     70   45       http://rumahdijual.com/depok/1116445-cluster-baru-di-bedahantugu-depok-murah.html                           
    400     70   45       http://rumahdijual.com/depok/1108514-rumah-murah-di-daerah-depok.html                                       
    400     70   45       http://rumahdijual.com/depok/1297376-rumah-murah-dp-suka2.html                                              
    400     70   42       http://rumahdijual.com/depok/883260-rumah-dengan-harga-terjangkau-di-tanah-baru-depok.html                  
    400     70   40       http://rumahdijual.com/depok/1314570-rumah-murah-cilodong-jatimulya-lokasi-strategis-rh343.html             
    400     70   40       http://rumahdijual.com/depok/1314599-rumah-depok-jatimulya-murah-lokasi-strategis-rh343.html                
    400     70   40       http://rumahdijual.com/depok/1312329-rumah-murah-dan-asri-di-sekitar-gdc-depok.html                         
    400     70   40       http://rumahdijual.com/depok/955236-rumah-minimalis-di-depok.html                                           
    400     66   36       http://rumahdijual.com/depok/1305856-rumah-cakep-harga-murah-di-cimanggis.html                              
    400     63   42       http://rumahdijual.com/depok/937325-rumah-baru-siap-huni-kpr-pancoran-mas-depok-lama.html                   
    400     46   41       http://rumahdijual.com/depok/1230928-rumah-murah-di-depok-jalan-raya-bogor-lokasi-perumahan.html            
    400     45   45       http://rumahdijual.com/depok/1161430-cluster-radiva-residence-pekapuran-depok.html                          
    400     1    45       http://rumahdijual.com/depok/993367-rumah-depok-citayam-harga-nego-lokasi-strategis.html
    

## House Price Between 400 - 500 Mio IDR

### Visualize Data


```python
df = visualizeData('depok', 400, 500);
```


![png](png/output_41_0.png)


### Analyze the Data of House Price Between 400 - 500 Mio IDR


```python
avg = averageMeasures(df)
```

    
    AVERAGE MEASURES
    -----------------
    
    building    55
        land    88
       price   454
    


```python
mostSpacious(df)
```

    
    MOST SPACIOUS LAND
    -----------------
    
        bath     5
         bed     5
    building   200
        land   400
       price   450
         url   http://rumahdijual.com/depok/1113622-rumah-kontrakan-5-pintu-aman-dan-nyaman-sawangan-depok.html
    
    MOST SPACIOUS BUILDING
    -----------------
    
        bath     1
         bed     3
    building   250
        land   200
       price   500
         url   http://rumahdijual.com/depok/1307113-di-jual-rumah-jalan-raya-pekapuran-siap-huni.html
    


```python
selectEconomical(df, avg, unit)
```

    
    MOST ECONOMICAL
    -----------------
    is when the price is really below average: 454 (million IDR) but you get above the average land: 88 (square meters) and above the average building: 55 (square meters)
    
    You are blessed to choose one of these 169  houses:
    
    price  land building                                                                                                        url
    400     99    80       http://rumahdijual.com/depok/776567-rumah-di-perumnas-depok-2-a.html                                    
    400     96    60       http://rumahdijual.com/depok/785630-di-jual-rumah-strategis-di-wilayah-depok.html                       
    400     94    72       http://rumahdijual.com/depok/1209699-rumah-cluster-cantik-kualitas-baik-harga-menarik.html              
    400     92    80       http://rumahdijual.com/depok/399403-rumah-dijual-komplek-tanah-baru.html                                
    400     90    80       http://rumahdijual.com/depok/1051720-perumnas-depok-timur.html                                          
    400     90    60       http://rumahdijual.com/depok/974927-rumah-cluster.html                                                  
    400     90    60       http://rumahdijual.com/depok/1069039-rumah-baru-asri-gede-3-kamar-siap-huni-di.html                     
    400     180   120      http://rumahdijual.com/depok/1254066-dijual-rumah-di-tapos-depok.html                                   
    400     170   170      http://rumahdijual.com/depok/1246382-rumah-lt-170-lb-170-di-dekat-setu-cilangkap.html                   
    400     164   95       http://rumahdijual.com/depok/1265200-rumah-murah-di-cipayung-depok.html                                 
    400     164   95       http://rumahdijual.com/depok/863117-rumah-murah-cipayung-depok.html                                     
    400     160   80       http://rumahdijual.com/depok/724422-cang-cing-ade-rumah-dijual-nih.html                                 
    400     150   70       http://rumahdijual.com/depok/724140-di-jual-rumah-tanah-cilodong-76-a.html                              
    400     144   100      http://rumahdijual.com/depok/1139330-dijual-rumah-di-bojongsari.html                                    
    400     140   140      http://rumahdijual.com/depok/1118140-rumah-di-depok-2-tengah.html                                       
    400     139   100      http://rumahdijual.com/depok/923316-dijual-cepat-rumah-di-depok-ii.html                                 
    400     135   100      http://rumahdijual.com/depok/1098417-rumah-murah-dijual-di-gang-jambu-rt-rw-03-a.html                   
    400     125   60       http://rumahdijual.com/depok/1274322-rumah-cluster-permata-rubby-2-dekat-stasiun.html                   
    400     121   70       http://rumahdijual.com/depok/969446-hunian-asri-harga-terjangkau-di-depok.html                          
    400     119   150      http://rumahdijual.com/depok/1257539-di-jual-rumah-siap-huni-di-jalan-di-jalan.html                     
    400     118   90       http://rumahdijual.com/depok/1284009-rumah-3-kamar-tidur-garasi-2-mobil-depan-rsud.html                 
    400     118   57       http://rumahdijual.com/depok/999159-rumah-harga-murah-di-depok-jawa-barat.html                          
    400     110   72       http://rumahdijual.com/depok/1096688-hunian-baru-dan-minimalis-lokasi-strategis-di-depok.html           
    400     110   60       http://rumahdijual.com/depok/942674-rumah-murah-depok-lama.html                                         
    400     107   70       http://rumahdijual.com/depok/889672-dijual-rumah-1-lantai-di-jalan-keadilan-rawa-denok.html             
    400     105   105      http://rumahdijual.com/depok/989178-rumah-jl-poin-mas.html                                              
    400     103   70       http://rumahdijual.com/depok/1310140-rumah-baru-siap-huni-di-rangkapan-jaya-harga-murah.html            
    400     100   90       http://rumahdijual.com/depok/901812-kontrakan-murah.html                                                
    400     100   70       http://rumahdijual.com/depok/1308918-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html              
    400     100   70       http://rumahdijual.com/depok/1308943-rumah-pasti-fotonya-asli-di-pitara-pancoran-mas-depok.html         
    400     100   70       http://rumahdijual.com/depok/1309001-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html              
    400     100   70       http://rumahdijual.com/depok/1309113-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html              
    400     100   70       http://rumahdijual.com/depok/1309256-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html              
    400     100   70       http://rumahdijual.com/depok/1309579-rumah-pasti-fotonya-asli-di-pitara-pancoran-mas-depok.html         
    400     100   70       http://rumahdijual.com/depok/1315828-rumah-pasti-di-pitara-pancoran-mas-depok.html                      
    400     100   70       http://rumahdijual.com/depok/1308889-rumah-pasti-fotonya-asli-di-pitara-pancoran-mas-depok.html         
    400     100   70       http://rumahdijual.com/depok/1308877-rumah-pasti-fotonya-asli-di-pitara-pancoran-mas-depok.html         
    400     100   70       http://rumahdijual.com/depok/1308842-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html              
    400     100   70       http://rumahdijual.com/depok/1308760-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html              
    400     100   70       http://rumahdijual.com/depok/1308553-rumah-pasti-sesuai-foto-di-pitara-depok.html                       
    400     100   70       http://rumahdijual.com/depok/1308575-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html              
    400     100   70       http://rumahdijual.com/depok/1308676-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html              
    400     100   70       http://rumahdijual.com/depok/1308736-siap-huni-dan-surat-jelas-di-pitara-pancoran-mas.html              
    410     111   90       http://rumahdijual.com/depok/1059179-rumah-di-mampang-depok-second.html                                 
    412     132   65       http://rumahdijual.com/depok/905378-rumah-asri-dan-siap-huni-di-mampang-depok.html                      
    415     90    70       http://rumahdijual.com/depok/1098761-rumah-nyaman-murah-di-di-perumahan-sukatani-permai-r21.html        
    415     125   150      http://rumahdijual.com/depok/986658-rumah-lantai-2-murah.html                                           
    415     121   70       http://rumahdijual.com/depok/962161-rumah-luasa-harga-ekonomis-dicimanggis.html                         
    420     95    60       http://rumahdijual.com/depok/1079873-mau-rumah-kamar-3-harga-kamar-2-disini-ada.html                    
    420     95    60       http://rumahdijual.com/depok/1070163-jual-rumah-siap-huni-400-juta.html                                 
    420     92    70       http://rumahdijual.com/depok/1104938-dijual-rumah-murah-di-bukit-golf-pekapuran.html                    
    420     90    70       http://rumahdijual.com/depok/730229-rumah-second-griya-devi.html                                        
    420     90    180      http://rumahdijual.com/depok/977409-rumah-lokasi-strategis-wilayah-cipayung-depok.html                  
    420     175   160      http://rumahdijual.com/depok/707742-rumah-gede-4-kamar-dekat-stasiun-citayam-pemilik-langsung.html      
    420     150   150      http://rumahdijual.com/depok/1055959-di-jual-rumah-asri-suasana-pedesaan-di-pondok-rajeg.html           
    420     118   70       http://rumahdijual.com/depok/589231-rumah-kavling-cinangka-depok.html                                   
    420     108   85       http://rumahdijual.com/depok/1263823-rumah-di-cinangka.html                                             
    420     102   60       http://rumahdijual.com/depok/1087909-rumah-bangunan-baru-bebas-biaya-surat-cipayung-depok.html          
    420     100   60       http://rumahdijual.com/depok/946635-rumah-minimalis-harga-ekonomis.html                                 
    425     90    90       http://rumahdijual.com/depok/796253-rumah-di-mampang-bojong-pancoran-mas.html                           
    425     90    60       http://rumahdijual.com/depok/1278917-dijual-rumah-di-bukit-rivaria-sawangan-depok.html                  
    425     89    60       http://rumahdijual.com/depok/1313150-puri-bali-sawangan-jual-cepaaat.html                               
    425     145   100      http://rumahdijual.com/depok/960084-di-jual-rumah-kpr-siap-huni-lt-145m-lb.html                         
    425     140   100      http://rumahdijual.com/depok/960078-di-jual-rumah-kpr-siap-huni-lt-140m-lb.html                         
    425     138   100      http://rumahdijual.com/depok/960095-di-jual-rumah-ready-stock-kpr-lt-138m-lb.html                       
    425     125   65       http://rumahdijual.com/depok/1313398-stop-beli-rumah-asal-asalan.html                                   
    425     125   65       http://rumahdijual.com/depok/1313388-rumah-cluster-permata-rubby-2-dekat-stasiun.html                   
    425     125   65       http://rumahdijual.com/depok/1310484-rumah-cluster-permata-rubby-2-dekat-stasiun.html                   
    425     125   65       http://rumahdijual.com/depok/1308216-rumah-cluster-murah-dekat-stasiun.html                             
    425     125   65       http://rumahdijual.com/depok/1305225-permata-rubby-2-7-menit-menuju-stasiun.html                        
    425     125   65       http://rumahdijual.com/depok/1101597-rumah-dalam-cluster.html                                           
    425     125   65       http://rumahdijual.com/depok/1313390-rumah-cluster-no-tipu-tipu.html                                    
    425     125   100      http://rumahdijual.com/depok/1199651-di-jual-rumah.html                                                 
    425     118   75       http://rumahdijual.com/depok/1078103-rumah-siap-huni-depok.html                                         
    430     90    90       http://rumahdijual.com/depok/1143556-rumah-dilokasi-strategis-perumnas-2-depok-krakatau-depok.html      
    430     90    90       http://rumahdijual.com/depok/1147953-rumah-lokasi-strategis-perumnas-2-depok.html                       
    430     90    60       http://rumahdijual.com/depok/682243-rumah-kpr-cluster-di-pusat-kota-depok.html                          
    430     90    60       http://rumahdijual.com/depok/917362-rumah-nyaman-murah-strategis.html                                   
    430     203   165      http://rumahdijual.com/depok/1019018-rumah-idaman-paling-murah.html                                     
    430     120   120      http://rumahdijual.com/depok/1152613-rumah-2-lantai-di-cipayung-depok.html                              
    430     120   120      http://rumahdijual.com/depok/1186011-rumah-di-depok-2-lantai-cuma-430jt.html                            
    430     120   120      http://rumahdijual.com/depok/1186600-rumah-di-depok-tanah-120m2.html                                    
    430     120   110      http://rumahdijual.com/depok/1189439-rumah-4-kamar-tanah-120-m2.html                                    
    430     108   72       http://rumahdijual.com/depok/1017246-taman-anyelir-2-depok.html                                         
    430     102   70       http://rumahdijual.com/depok/1290921-sawangan-permai-lt-102-m2-430-juta.html                            
    435     96    96       http://rumahdijual.com/depok/1278817-rumah-second-murah-dan-luas-di-dekat-tol-cijago.html               
    435     95    60       http://rumahdijual.com/depok/962479-kavling-h-kocen-siapa-cepat-dia-dapat.html                          
    435     118   56       http://rumahdijual.com/depok/918209-rumah-sukmajaya-depok.html                                          
    435     112   88       http://rumahdijual.com/depok/1246882-rumah-bisa-buat-usaha-di-pinggir-jalan.html                        
    435     110   60       http://rumahdijual.com/depok/1175460-rumah-second-di-depok-kelapa-dua.html                              
    435     105   60       http://rumahdijual.com/depok/928098-rumah-cluster-murah-di-raden-saleh-depok-dekat-rs.html              
    435     100   60       http://rumahdijual.com/depok/1301739-rumah-di-belakang-dtc-depok.html                                   
    435     100   60       http://rumahdijual.com/depok/1301915-rumah-dekat-dtc-depok-jalan-mampang.html                           
    440     110   60       http://rumahdijual.com/depok/813060-rumah-ready-stock-3-kammar-tidur.html                               
    440     110   60       http://rumahdijual.com/depok/817475-rumah-cluster-cipayung-depok.html                                   
    440     101   80       http://rumahdijual.com/depok/1247507-rumah-murah-di-tanah-baru-sangat-dekat-ke-jalan.html               
    440     100   60       http://rumahdijual.com/depok/962308-rumah-cluster-kota-depok.html                                       
    445     97    72       http://rumahdijual.com/depok/1085651-rumah-elit-harga-gak-bikin-sulit.html                              
    450     98    70       http://rumahdijual.com/depok/1220888-rumah-second-diwadas-pitara-harga-maknyossss.html                  
    450     98    65       http://rumahdijual.com/depok/1287904-rumah-cantik-bsa-cicil.html                                        
    450     97    72       http://rumahdijual.com/depok/1301775-rumah-murah-di-depok-siap-huni.html                                
    450     97    72       http://rumahdijual.com/depok/1301891-rumah-siap-huni-type-97-72-450-juta-nego.html                      
    450     96    96       http://rumahdijual.com/depok/1067327-jual-cepat-minggu-ini-butuh-uang-mau-keluar-kota.html              
    450     96    70       http://rumahdijual.com/depok/898399-rumah-dijual-cepat.html                                             
    450     96    60       http://rumahdijual.com/depok/1043114-rumah-dijual-cepat.html                                            
    450     95    60       http://rumahdijual.com/depok/928533-hunian-asri-di-depok-kavling-jatimulya.html                         
    450     94    90       http://rumahdijual.com/depok/1164014-rumah-warung-type-90-94-di-jatijajar-depok-siap.html               
    450     94    72       http://rumahdijual.com/depok/1161926-mutiara-jaya-residence-jemb-serong.html                            
    450     94    72       http://rumahdijual.com/depok/1231714-depok-bulak-timur-rumah-dekat-pasar-grosir-dan-jalur.html          
    450     94    72       http://rumahdijual.com/depok/1237780-depok-bulak-timur-rumah-siap-huni-dekat-jalur-angkot.html          
    450     90    90       http://rumahdijual.com/depok/1027734-lelang-rumah-likuidasi-komplek-bdn-rangkapan-jaya-pancoran-mas.html
    450     90    87       http://rumahdijual.com/depok/336269-rumah-minimalis-strategis-depok-timur.html                          
    450     90    85       http://rumahdijual.com/depok/1018569-rumah-murah-di-beji-depok.html                                     
    450     90    80       http://rumahdijual.com/depok/920727-rumah-murah-di-pancoran-mas-pitara-cipayung-wadas-depok.html        
    450     90    80       http://rumahdijual.com/depok/1092647-rumah-murah-beji-depok-property-syariah.html                       
    450     90    75       http://rumahdijual.com/depok/1132534-rumah-murah-di-depok.html                                          
    450     90    75       http://rumahdijual.com/depok/1132524-rumah-besar-harga-kecil-dekat-stasiun.html                         
    450     90    70       http://rumahdijual.com/depok/1060984-rumah-baru-banyak-bonusnya-di-limo-cinere-depok.html               
    450     90    60       http://rumahdijual.com/depok/1148919-rumah-baru-siap-huni-banyak-bonusnya-di-limo-cinere.html           
    450     90    60       http://rumahdijual.com/depok/1221208-rumah-cluster-depok-pitara-raya.html                               
    450     90    130      http://rumahdijual.com/depok/1043463-rumah-setrategis-harga-sangat-ekonomis-di-depok.html               
    450     90    115      http://rumahdijual.com/depok/1065153-dijual-rumah-sangat-strategis-di-depok.html                        
    450     400   200      http://rumahdijual.com/depok/1113622-rumah-kontrakan-5-pintu-aman-dan-nyaman-sawangan-depok.html        
    450     200   200      http://rumahdijual.com/depok/1153126-rumah-keluarga-4-kamar-tidur-bertanah-luas-di-pancoran.html        
    450     157   127      http://rumahdijual.com/depok/575441-rumah-dijual-murah-di-depok-dekat-masjid-kubah-mas.html             
    450     150   72       http://rumahdijual.com/depok/1065302-rumah-siap-huni-asri-nyaman-strategis-dekat-water-park.html        
    450     145   70       http://rumahdijual.com/depok/1067162-rumah-secondary-akses-mudah-50-meter-ke-jalan-raya.html            
    450     140   140      http://rumahdijual.com/depok/920383-rumah-kavleling-di-mampang-depok.html                               
    450     130   70       http://rumahdijual.com/depok/1016858-rumah-mewah-harga-sederhana.html                                   
    450     125   65       http://rumahdijual.com/depok/1077015-rumah-cluster-100-baru.html                                        
    450     125   65       http://rumahdijual.com/depok/1093848-rumah-manis-harga-ekonomis.html                                    
    450     125   65       http://rumahdijual.com/depok/1207030-rumah-baru-harga-lama.html                                         
    450     125   65       http://rumahdijual.com/depok/1093869-rumah-murah-cluster-kota-depok.html                                
    450     120   90       http://rumahdijual.com/depok/318290-rumah-bagus-bertanah-besar-di-rangkapan-jaya-baru-pancoran.html     
    450     120   60       http://rumahdijual.com/depok/1070818-rumah-di-jual-sawangan-depok.html                                  
    450     120   60       http://rumahdijual.com/depok/1070828-rumah-di-jual-sawangan-depok.html                                  
    450     113   60       http://rumahdijual.com/depok/1174065-rumah-luas-dekat-stasiun-depok.html                                
    450     113   60       http://rumahdijual.com/depok/1218508-rumah-luas-harga-puas-kota-depok.html                              
    450     112   70       http://rumahdijual.com/depok/1016841-rumah-cluster-paling-strategis.html                                
    450     112   100      http://rumahdijual.com/depok/978446-rumah-setartegis-harga-murah.html                                   
    450     110   75       http://rumahdijual.com/depok/1298082-rumah-di-jual-dekat-grand-depok-city-gdc-depok.html                
    450     110   72       http://rumahdijual.com/depok/1251911-tumah-luas-harga-ga-bkin.html                                      
    450     110   60       http://rumahdijual.com/depok/886562-dijual-rumah-asri-di-taman-anyelir-2-depok.html                     
    450     106   90       http://rumahdijual.com/depok/1129833-rumah-murah-bisa-kpr-dekat-mall-dtc-depok.html                     
    450     105   90       http://rumahdijual.com/depok/788218-rumah-di-tanah-baru-beji-depok.html                                 
    450     105   80       http://rumahdijual.com/depok/1293198-rumah-masuk-mobil-siap-huni-di-kalimulya-depok-r21.html            
    450     105   80       http://rumahdijual.com/depok/1195601-dijual-santai-rumah-hook-di-kampung-duren-dekat-gdc.html           
    450     105   63       http://rumahdijual.com/depok/999885-rumah-baru-siap-huni.html                                           
    450     104   70       http://rumahdijual.com/depok/833575-rumah-cantik-minimalis-di-maharaja-depok.html                       
    450     103   60       http://rumahdijual.com/depok/714147-rumah-siap-huni-di-komplek-perumahan-sawangan-depok.html            
    450     102   80       http://rumahdijual.com/depok/927642-rumah-sawangan-permai-promo.html                                    
    450     102   65       http://rumahdijual.com/depok/1107733-rumah-mewah-harga-rendah-di-depok.html                             
    450     101   90       http://rumahdijual.com/depok/839435-rumah-dijual-di-tanah-baru-beji.html                                
    450     100   90       http://rumahdijual.com/depok/1018965-rumah-siap-huni-di-lembah-hijau.html                               
    450     100   90       http://rumahdijual.com/depok/1108904-rumah-murah-siap-huni-depok.html                                   
    450     100   80       http://rumahdijual.com/depok/1252355-di-jual-rumah-minmalis-harga-bersahabat-di-kalimulya-depok.html    
    450     100   78       http://rumahdijual.com/depok/1069777-rumah-2-lantai-rawakalong-depok.html                               
    450     100   70       http://rumahdijual.com/depok/1048198-rumah-di-cipayung-depok.html                                       
    450     100   70       http://rumahdijual.com/depok/1048452-rumah-dijual-murah-di-cipayung-depok.html                          
    450     100   70       http://rumahdijual.com/depok/1063940-rumah-murah-di-perumahan-permata-depok.html                        
    450     100   70       http://rumahdijual.com/depok/1101552-rumah-pitara-kota-depok.html                                       
    450     100   70       http://rumahdijual.com/depok/1167726-di-jual-rumah-cipayung-depok.html                                  
    450     100   70       http://rumahdijual.com/depok/1225868-rumah-minimalis-pondok-cabe.html                                   
    450     100   67       http://rumahdijual.com/depok/1172259-rumah-gede-3-kamar-tidur-baru-siap-huni-di.html                    
    450     100   60       http://rumahdijual.com/depok/1099480-rumah-bebas-banjir-dekat-jalan-raya.html                           
    450     100   60       http://rumahdijual.com/depok/1223591-rumah-berkualitas.html                                             
    450     100   60       http://rumahdijual.com/depok/850976-rumah-murah-siap-huni-di-sawangan.html                              
    450     100   60       http://rumahdijual.com/depok/1079079-rumah-nyaman-harga-obral.html                                      
    450     100   100      http://rumahdijual.com/depok/936233-rumah-perumnas-3-depok-timur.html
    


```python
selectModerate(df, avg, unit)
```

    
    MODERATE PRICE
    -----------------
    is when the price is above average: 454 (million IDR) with above-average land: 88 (square meters) and above-average building: 55 (square meters)
    
    
    There are : 420  items with above-average price and above-average land.
    
    There are : 279  items with above-average price, above-average land and above-average building.
    
    price  land building                                                                                                          url
    460     96    80       http://rumahdijual.com/depok/796456-rumah-baru-minimalis-murah-di-pancoran-mas-depok-dekat.html           
    460     96    180      http://rumahdijual.com/depok/370371-rumah-shm-minimalis-harga-murah-di-depok.html                         
    460     95    60       http://rumahdijual.com/depok/982706-rumah-minimalis-siap-huni-dekat-stasiun-keretai-depok.html            
    460     91    90       http://rumahdijual.com/depok/1240852-rumah-mewah-murah-strategis-15-menit-ke-stasiun-depok.html           
    460     90    80       http://rumahdijual.com/depok/1078415-rumah-indah-suasana-asri.html                                        
    460     90    80       http://rumahdijual.com/depok/924180-depok-timur-460-juta.html                                             
    460     280   150      http://rumahdijual.com/depok/844123-rumah-murah-di-depok.html                                             
    460     120   120      http://rumahdijual.com/depok/848586-kontrakan-4-petak-dekat-ke-stasiun-depok-lama.html                    
    465     90    55       http://rumahdijual.com/depok/1108303-desember-sale-jual-rumah-baru-design-menarik-harga-murah.html        
    465     115   100      http://rumahdijual.com/depok/709829-rumah-2-lantai-nyaman-dan-asri-dekat-gdc-depok.html                   
    465     105   65       http://rumahdijual.com/depok/1277013-rumah-di-depok-dengan-suasan-pedesaan.html                           
    465     104   70       http://rumahdijual.com/depok/1182966-rumah-ready-pinggir-jalan-lokasi-strategis-dekat-masjid-kubah.html   
    465     103   80       http://rumahdijual.com/depok/1265068-rumah-murah-dan-siap-huni-dekat-dtc-sawangan.html                    
    465     103   80       http://rumahdijual.com/depok/872076-rumah-murah-dan-siap-huni-dekat-dtc-sawangan-pancoran.html            
    465     100   60       http://rumahdijual.com/depok/810967-cluster-nyaman-harga-teman-lokasi-aman-dekat-stasiun-depok.html       
    465     100   60       http://rumahdijual.com/depok/1203803-rumah-baru-dipitara-depok-100-m2-masuk-mobil-berikut.html            
    467     90    90       http://rumahdijual.com/depok/881707-rumah-murah-banget-di-depok.html                                      
    470     95    90       http://rumahdijual.com/depok/796886-dijual-cepat-rumah-siap-huni-masuk-mobil-rangkapan-jaya.html          
    470     90    90       http://rumahdijual.com/depok/1214464-rumah-di-bakti-jaya-sukmajaya-depok.html                             
    470     90    80       http://rumahdijual.com/depok/1246188-perumnas-depok-2-tengah-50-meter-jalur-angkot-24-a.html              
    470     90    60       http://rumahdijual.com/depok/1246171-perumnas-depok-2-tengah-100-meter-jalur-angkot-24-a.html             
    470     160   150      http://rumahdijual.com/depok/696588-rumah-lama-namun-kokoh.html                                           
    470     120   60       http://rumahdijual.com/depok/918942-rumah-baru-kokoh-dan-bernilai.html                                    
    470     120   55       http://rumahdijual.com/depok/243271-cluster-puri-rawa-denok.html                                          
    470     120   55       http://rumahdijual.com/depok/636866-cluster-puri-rawa-denok-free-kpr-dan-bphtb-tanah.html                 
    470     105   60       http://rumahdijual.com/depok/1255320-rumah-di-depok.html                                                  
    470     103   70       http://rumahdijual.com/depok/1026684-bu-rumah-murah-di-sawangan-depok.html                                
    472     105   60       http://rumahdijual.com/depok/1298929-rumah-3-kamar-tidur-di-depok.html                                    
    475     95    105      http://rumahdijual.com/depok/892176-rumah-minimalis-kota-depok.html                                       
    475     90    90       http://rumahdijual.com/depok/844257-perumnas-depok-2-tengah-50-meter-jalur-angkot-24-a.html               
    475     90    85       http://rumahdijual.com/depok/1042874-rumah-murah-pancoran-mas-depok.html                                  
    475     90    82       http://rumahdijual.com/depok/949802-cluster-di-depok.html                                                 
    475     90    80       http://rumahdijual.com/depok/1078977-rumah-siap-huni-10-menit-ke-stasiun-ka-depok.html                    
    475     90    60       http://rumahdijual.com/depok/1079941-rumah-di-meruyung-limo-depok-lingkungan-nyaman.html                  
    475     90    115      http://rumahdijual.com/depok/1153863-rumah-dijual-pdk-sukatani-permai.html                                
    475     89    60       http://rumahdijual.com/depok/1088861-rumah-idaman-keluarga-sakinah.html                                   
    475     88    72       http://rumahdijual.com/depok/1174581-rumah-baru-di-villa-arsip-pancoran-mas-depok.html                    
    475     300   220      http://rumahdijual.com/depok/426706-rumah-besar-harga-minimal-dekat-pasar-parung.html                     
    475     300   200      http://rumahdijual.com/depok/980759-rumah-besar-5kamar-sawangan.html                                      
    475     250   100      http://rumahdijual.com/depok/1052991-rumah-murah-cantik-di-pondok-rajeg-kalimulya-depok-r21.html          
    475     153   100      http://rumahdijual.com/depok/1157155-rumah-tingkat-murah-dekat-grand-depok-city.html                      
    475     124   100      http://rumahdijual.com/depok/694147-rumah-murah-dijual-cepat-di-cimanggis.html                            
    475     110   72       http://rumahdijual.com/depok/1246248-rumah-di-dalam-perumahan-regency-depok.html                          
    475     110   65       http://rumahdijual.com/depok/1247673-rumah-di-dalam-cluster-mantap.html                                   
    475     110   65       http://rumahdijual.com/depok/1079526-rumah-cluster-pitara-raya-depok-pancoran-mas.html                    
    475     105   65       http://rumahdijual.com/depok/1104082-rumah-bebas-banjir-di-depok.html                                     
    475     105   65       http://rumahdijual.com/depok/1105506-one-gate-system-aman-itu-no-satu.html                                
    475     105   65       http://rumahdijual.com/depok/1313532-rumah-3-kamar-tidur-di-depok.html                                    
    475     104   78       http://rumahdijual.com/depok/997067-rumah-cluster-take-over-kredit-depok.html                             
    475     100   150      http://rumahdijual.com/depok/1246947-rumah-tingkat-strategis-dekat-stasiun.html                           
    480     91    95       http://rumahdijual.com/depok/1196596-dijual-cepat-rumah-second-2-lantai-di-cluster-depok.html             
    480     90    90       http://rumahdijual.com/depok/855010-rumah-dijual-rumah-sangat-murah-baru-renovasi-di-depok.html           
    480     90    70       http://rumahdijual.com/depok/1246168-perumnas-depok-timur-100-meter-ke-jalur-angkot-24-a.html             
    480     160   140      http://rumahdijual.com/depok/1250010-rumah-masuk-mobil-di-raden-saleh-depok-r21-0449-a.html               
    480     150   60       http://rumahdijual.com/depok/1261172-dijual-cepat-rumah-tumbuh.html                                       
    480     140   120      http://rumahdijual.com/depok/1035614-rumah-dekat-stasiun-citayam-areasekitar-permata-depok.html           
    480     130   80       http://rumahdijual.com/depok/1139398-dijual-rumah-akses-dekat-dengan-jalan-tol.html                       
    480     105   85       http://rumahdijual.com/depok/989233-rumah-bagus-harga-ok.html                                             
    480     104   60       http://rumahdijual.com/depok/1232691-rumah-baru-dekat-permata-regentcydepok.html                          
    480     102   70       http://rumahdijual.com/depok/771819-perumnas-depok-timur-100-meter-ke-jalur-angkot-24-a.html              
    480     100   90       http://rumahdijual.com/depok/1300433-rumah-minimalis-di-jl-rawa-indah-depok-siap-huni.html                
    485     120   100      http://rumahdijual.com/depok/1058081-rumah-siap-huni-dekat-pinggir-jalan-raya-kali-licin.html             
    485     110   180      http://rumahdijual.com/depok/971448-dijual-cepat-semi-furnished-owner-langsung.html                       
    485     105   65       http://rumahdijual.com/depok/1079653-rumah-cluster-di-jalan-raya-bojong-ratu-jaya-depok.html              
    489     326   90       http://rumahdijual.com/depok/1168905-rumah-kontrakan-3-pintu-bertanah-luas-sawangan-depok.html            
    490     89    65       http://rumahdijual.com/depok/794936-rumah-modern-di-jalan-perintis-poncol-tanah-baru-depok.html           
    490     141   80       http://rumahdijual.com/depok/1216568-di-jual-rumah-murah-tanah-luas-di-permata-depok.html                 
    490     140   70       http://rumahdijual.com/depok/891801-rumah-mewah-harga-murah.html                                          
    490     103   56       http://rumahdijual.com/depok/716124-rumah-dijual-bbm-tole-iskandar-dekat-tol-cijago.html                  
    490     100   97       http://rumahdijual.com/depok/1119194-rumah-memukau-harga-terjangkau-di-cimanggis.html                     
    490     100   70       http://rumahdijual.com/depok/1037015-rumah-dijual-di-komplek-adhy-karya-depok.html                        
    495     91    64       http://rumahdijual.com/depok/1110119-baru-minimalis-modern-type-60-2-lantai-di-pondok.html                
    495     90    55       http://rumahdijual.com/depok/1299664-di-jual-rumah-minimalis-siap-huni-tanpa-renovasi-di.html             
    495     135   135      http://rumahdijual.com/depok/1068025-rumah-lokasinya-pinggir-jalan-carportnya-masuk-2-mobil.html          
    495     113   60       http://rumahdijual.com/depok/1004647-rumah-minimalis-dekat-stasiun-depok-lama-sertifikat-hak-milik.html   
    495     105   100      http://rumahdijual.com/depok/821760-rumah-di-bukit-cengkeh-1-cimanggis-depok-dekat-tol.html               
    495     103   82       http://rumahdijual.com/depok/806286-cluster-cantik-di-pancoran-mas-depok-lokasi-strategis-murah.html      
    495     101   80       http://rumahdijual.com/depok/1283568-rumah-cantik-masuk-mobil-di-raden-saleh-depok-r21.html               
    497     123   100      http://rumahdijual.com/depok/1110460-rumah-murah-pitara-pancoran-mas-depok.html                           
    499     220   120      http://rumahdijual.com/depok/1129436-rumah-murah-depok-cipayung-jembatan-serong-nempel-jalur-angkot.html  
    499     108   126      http://rumahdijual.com/depok/896313-rumah-di-jual-murah-perumahan-strategis-di-depok-bonus.html           
    500     98    65       http://rumahdijual.com/depok/1279602-rumah-cantik-siap-huni-di-jl-perjuangan-dekat-villa.html             
    500     96    90       http://rumahdijual.com/depok/900871-rumah-ditapos-depok-nyaman-dilingkungan-asri-dengan-keamanan-full.html
    500     95    63       http://rumahdijual.com/depok/1273992-rumah-di-depok.html                                                  
    500     95    60       http://rumahdijual.com/depok/1313937-rumah-siap-masuk-di-cibinong-dekat-pemda-cibinong.html               
    500     95    60       http://rumahdijual.com/depok/1103999-rumah-baru-sawangan-depok-aset-bagus.html                            
    500     95    57       http://rumahdijual.com/depok/951333-rumah-ready-stock-di-belakang-kostrad-depok-tinggal-angkat.html       
    500     95    55       http://rumahdijual.com/depok/883262-rumah-dengan-harga-terjangkau-dekat-stasiun-depok-lama.html           
    500     91    56       http://rumahdijual.com/depok/875088-perumahan-cluster-lokasi-strategis-kota-depok.html                    
    500     90    75       http://rumahdijual.com/depok/1256535-dijual-rumah-di-perumas-2-depok.html                                 
    500     90    70       http://rumahdijual.com/depok/1261538-bukit-rivaria-500-juta-full-renovasi.html                            
    500     90    60       http://rumahdijual.com/depok/1261181-bukit-rivaria.html                                                   
    500     377   250      http://rumahdijual.com/depok/1000412-rumah-murah-di-depok.html                                            
    500     309   90       http://rumahdijual.com/depok/891528-rumah-murah-di-tapos-depok.html                                       
    500     309   90       http://rumahdijual.com/depok/855076-dijual-rumah-murah-di-tapos-depok.html                                
    500     200   70       http://rumahdijual.com/depok/1305120-rumah-dijual-kampung-kebon-cinangka-dekat-kubah-emas-sawangan.html   
    500     200   250      http://rumahdijual.com/depok/1307113-di-jual-rumah-jalan-raya-pekapuran-siap-huni.html                    
    500     180   180      http://rumahdijual.com/depok/1058776-jual-cepat-rumah-siap-huni-di-sawangan-depok-bojongsari.html         
    500     160   90       http://rumahdijual.com/depok/971918-kavling-abdul-wahab-mengapa-tunggu-sampai-besok.html                  
    500     160   160      http://rumahdijual.com/depok/1088598-rumah-dekat-perapatan-uki-pitara.html                                
    500     151   60       http://rumahdijual.com/depok/695904-rumah-di-pancoran-mas-depok.html                                      
    500     150   75       http://rumahdijual.com/depok/1314614-di-jual-rumah-terjangkau-luas-tanah-150m-sawangan-depok.html         
    500     150   120      http://rumahdijual.com/depok/733955-rumah-bekas-daerah-pondok-petir-depok-ada-warungnya.html              
    500     150   100      http://rumahdijual.com/depok/889788-rumah-dijual-cepat-bu.html                                            
    500     140   70       http://rumahdijual.com/depok/1253000-luas-murah-asri-di-mekarsari-cimanggis.html                          
    500     139   70       http://rumahdijual.com/depok/1015868-rumah-siap-huni-3-kamar-di-pitara-depok.html                         
    500     135   120      http://rumahdijual.com/depok/1307861-urun-harga-rumah-di-sukatani-dari-600-jt-turun.html                  
    500     129   80       http://rumahdijual.com/depok/937422-cluster-permata-ruby.html                                             
    500     129   70       http://rumahdijual.com/depok/948519-rumah-luas-harga-murah.html                                           
    500     126   56       http://rumahdijual.com/depok/930894-rumah-baru-120-meter-kpr-depok-lama.html                              
    500     125   75       http://rumahdijual.com/depok/1051903-rumah-akses-tol-dan-lrt-cimanggis-de-residence.html                  
    500     122   75       http://rumahdijual.com/depok/876937-dijual-rumah-murah-strategis-perbatasan-depok-dan-jakarta.html        
    500     122   56       http://rumahdijual.com/depok/1173698-rumah-harga-murah-dan-banyak-keuntungan-di-depok.html                
    500     122   100      http://rumahdijual.com/depok/1142914-rumah-dijual-di-depok.html                                           
    500     120   56       http://rumahdijual.com/depok/1174706-rumah-murah-spesifikasi-premium-di-sawangan-depok.html               
    500     120   56       http://rumahdijual.com/depok/834014-rumah-baru-124-meter-siap-huni-depok-lama.html                        
    500     115   60       http://rumahdijual.com/depok/711402-rumah-minimalis-kota-depok.html                                       
    500     115   60       http://rumahdijual.com/depok/712810-rumah-cluster-modern-kota-depok.html                                  
    500     111   100      http://rumahdijual.com/depok/689239-rumah-dekat-stasiun-citayam-depok.html                                
    500     110   80       http://rumahdijual.com/depok/1301686-rumah-di-kali-mulya-depok-siap-huni.html                             
    500     110   80       http://rumahdijual.com/depok/1186555-rumah-di-kali-mulya-mandor.html                                      
    500     110   70       http://rumahdijual.com/depok/1050762-rumah-baru-110-mtr-kalimulya-dkt-gdc-depok.html                      
    500     110   60       http://rumahdijual.com/depok/323777-rumah-asri-nuansa-bali-untuk-keluarga-muda.html                       
    500     110   55       http://rumahdijual.com/depok/1043416-rumah-setrategis-harga-ekonomis-di-depok.html                        
    500     110   100      http://rumahdijual.com/depok/962364-rumah-minimalis-baru-cipayung-depok.html                              
    500     107   70       http://rumahdijual.com/depok/1259210-rumah-minimalis-3-kamar-tidur-2-kamar-mandi-dekat.html               
    500     107   70       http://rumahdijual.com/depok/1259209-rumah-manis-dekat-pusat-kota-depok.html                              
    500     107   70       http://rumahdijual.com/depok/1256573-hunian-minimalis-dekat-pusat-kota.html                               
    500     107   70       http://rumahdijual.com/depok/1256565-rumah-minimalis-dekat-pusat-kota.html                                
    500     107   70       http://rumahdijual.com/depok/1248255-rumah-luas-3-kamar-tidur-dekat-pusat-kota.html                       
    500     106   60       http://rumahdijual.com/depok/1121737-rumah-di-regency-depok.html                                          
    500     105   90       http://rumahdijual.com/depok/740291-di-jual-rumah-cantik-siap-huni-di-permata-depok.html                  
    500     105   70       http://rumahdijual.com/depok/1112380-rumah-ready-stock-di-jalan-raya-pitara-depok.html                    
    500     105   65       http://rumahdijual.com/depok/1108420-rumah-besar-3-kamar-harga-2-kamar-dekat-stasiun.html                 
    500     105   65       http://rumahdijual.com/depok/1038494-rumah-besar-3-kamar-harga-2-kamar-dekat-stasiun.html                 
    500     105   60       http://rumahdijual.com/depok/1062621-beli-rumah-dapat-mobil.html                                          
    500     104   70       http://rumahdijual.com/depok/1313392-permata-regency-kota-depok.html                                      
    500     104   70       http://rumahdijual.com/depok/1310542-stop-beli-rumah-dengan-foto-iklan-palsu.html                         
    500     104   70       http://rumahdijual.com/depok/1310507-stop-beli-rumah-dengan-foto-iklan-palsu-dan-harga.html               
    500     104   70       http://rumahdijual.com/depok/1310495-stop-beli-rumah-foto-palsu-harga-murah.html                          
    500     104   70       http://rumahdijual.com/depok/1310477-rumah-minimalis-dekat-pusat-kota-depok.html                          
    500     104   70       http://rumahdijual.com/depok/1305223-rumah-minimalis-bisa-dicicil-pribadi-ke-owner-langsung.html          
    500     104   65       http://rumahdijual.com/depok/1313402-rumah-cantik-dekat-pusat-kota.html                                   
    500     104   65       http://rumahdijual.com/depok/1118356-rumah-baru-harga-murah-tahun-sekarang-tahun-depan-mahal.html         
    500     104   65       http://rumahdijual.com/depok/1040296-rumah-lokasi-strategis-aman-dan-nyaman.html                          
    500     104   65       http://rumahdijual.com/depok/1036730-investasi-cerdas-untuk-masa-depan.html                               
    500     102   90       http://rumahdijual.com/depok/996103-dijual-rumah-di-depok-lokasi-strategis-5menit-dari-margonda.html      
    500     102   60       http://rumahdijual.com/depok/1046431-komplek-pertanian-depok.html                                         
    500     100   90       http://rumahdijual.com/depok/978724-rumah-dekat-jalan-raya-citayam-depok.html                             
    500     100   90       http://rumahdijual.com/depok/1231173-dijual-rumah-baru.html                                               
    500     100   80       http://rumahdijual.com/depok/1097213-properti-grya-pratama-asri-kota-depok.html                           
    500     100   80       http://rumahdijual.com/depok/1065338-rumah-cluster-depok-pitara.html                                      
    500     100   80       http://rumahdijual.com/depok/1064272-cluster-depok-30meter-ke-jalur-angkot.html                           
    500     100   80       http://rumahdijual.com/depok/1064106-rumah-cluster-pitara-kota-depok.html                                 
    500     100   80       http://rumahdijual.com/depok/1060871-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html          
    500     100   80       http://rumahdijual.com/depok/1060869-rumah-cluster-pitara-kota-depok.html                                 
    500     100   80       http://rumahdijual.com/depok/1058835-rumah-type-80-100-lokasi-strategis-depok.html                        
    500     100   80       http://rumahdijual.com/depok/1056815-cluster-murah-banyak-pilihan.html                                    
    500     100   80       http://rumahdijual.com/depok/1055491-rumah-cluster-di-pitara-kota-depok-strategis.html                    
    500     100   80       http://rumahdijual.com/depok/1055126-rumah-cluster-di-pitara-depok.html                                   
    500     100   80       http://rumahdijual.com/depok/1134295-rumah-tingkat-harga-gak-bikin-melarat.html                           
    500     100   80       http://rumahdijual.com/depok/1301724-rumah-di-depok-kali-mulya.html                                       
    500     100   80       http://rumahdijual.com/depok/1226248-mandala-golden-residence-sawangan-kota-depok-promo-discount-dp.html  
    500     100   80       http://rumahdijual.com/depok/1112478-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html         
    500     100   80       http://rumahdijual.com/depok/1094205-rumah-cluster-pancoran-mas-depok.html                                
    500     100   80       http://rumahdijual.com/depok/1115852-rumah-type-80-100-m-di-jln-pitara-pancoran.html                      
    500     100   80       http://rumahdijual.com/depok/1094200-rumah-cluster-kemana-mana-deket.html                                 
    500     100   80       http://rumahdijual.com/depok/1178394-rumah-ready-stock-tanah-100-a.html                                   
    500     100   80       http://rumahdijual.com/depok/1221211-rumah-cluster-one-gate-system.html                                   
    500     100   80       http://rumahdijual.com/depok/1221054-rumah-dekat-pusat-kota-depok.html                                    
    500     100   80       http://rumahdijual.com/depok/1092348-rumah-cluster-pitara-pancoran-mas-depok.html                         
    500     100   80       http://rumahdijual.com/depok/1083983-one-gate-system-cluster-pitara-pancoran-mas-kota-depok.html          
    500     100   80       http://rumahdijual.com/depok/1042700-rumah-cluster-pitara-depok-lantai-full-granit.html                   
    500     100   80       http://rumahdijual.com/depok/1042875-rumah-cluster-pitara-depok.html                                      
    500     100   80       http://rumahdijual.com/depok/1089183-hunian-nyaman-dan-asri-one-gate-system.html                          
    500     100   80       http://rumahdijual.com/depok/1044218-rumah-cluster-minimalis-di-pitara-depok.html                         
    500     100   80       http://rumahdijual.com/depok/1050675-rumah-cluster-pitara-depok.html                                      
    500     100   80       http://rumahdijual.com/depok/1083970-hunian-cluster-pitara-pancoran-mas-depok-one-gate-system.html        
    500     100   80       http://rumahdijual.com/depok/1078966-rumah-cluster-strategis-siapa-yang-suka.html                         
    500     100   80       http://rumahdijual.com/depok/1078548-rumah-cluster-one-gate-system-pitara-pancoran-mas-depok.html         
    500     100   80       http://rumahdijual.com/depok/1078466-rumah-cluster-one-gate-system-pitara-pancoran-mas-depok.html         
    500     100   80       http://rumahdijual.com/depok/1078412-rumah-cluster-one-gate-system-pitara-pancoran-mas-depok.html         
    500     100   80       http://rumahdijual.com/depok/1077652-rumah-cluster-pitara-pancoran-mas-depok.html                         
    500     100   80       http://rumahdijual.com/depok/1072831-cluster-100m2-pitara-depok.html                                      
    500     100   80       http://rumahdijual.com/depok/1072600-cluster-pitara-depok-nyaman-dan-bebas-banjir.html                    
    500     100   80       http://rumahdijual.com/depok/1070868-rumah-cluster-pitara-pancoran-mas-kota-depok.html                    
    500     100   80       http://rumahdijual.com/depok/1068230-rumah-cluster-pitara-kota-depok.html                                 
    500     100   80       http://rumahdijual.com/depok/1068182-rumah-cluster-pitara-kota-depok.html                                 
    500     100   80       http://rumahdijual.com/depok/1067256-rumah-di-depok-pitara.html                                           
    500     100   80       http://rumahdijual.com/depok/1056112-rumah-cluster-di-pitara-kota-depok-strategis.html                    
    500     100   80       http://rumahdijual.com/depok/1056086-rumah-cluster-pitara-kota-depok.html                                 
    500     100   80       http://rumahdijual.com/depok/1056044-rumah-cluster-pitara-kota-depok.html                                 
    500     100   80       http://rumahdijual.com/depok/1045264-rumah-cluster-di-pitara-kota-depok.html                              
    500     100   70       http://rumahdijual.com/depok/1112341-rumah-cluster-jalan-pitara-raya-kota-depok.html                      
    500     100   70       http://rumahdijual.com/depok/1112617-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html         
    500     100   70       http://rumahdijual.com/depok/1112602-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html         
    500     100   70       http://rumahdijual.com/depok/1112496-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html         
    500     100   70       http://rumahdijual.com/depok/1112468-rumah-cluster-jalan-pitara-pancoran-mas-depok.html                   
    500     100   70       http://rumahdijual.com/depok/1112460-rumah-cluster-pitara-pancoran-mas-kota-depok.html                    
    500     100   70       http://rumahdijual.com/depok/1112454-rumah-cluster-one-gate-system-pitara-pancoran-mas-depok.html         
    500     100   70       http://rumahdijual.com/depok/1137981-rumah-manis-gaya-minimalis-kota-depok.html                           
    500     100   70       http://rumahdijual.com/depok/1112449-hunian-cluster-one-gate-system.html                                  
    500     100   70       http://rumahdijual.com/depok/1112122-hunian-cluster-di-pitara-pancoran-mas-kota-depok.html                
    500     100   70       http://rumahdijual.com/depok/1110858-hunian-cluster-di-pitara-pancoran-mas-kota-depok.html                
    500     100   70       http://rumahdijual.com/depok/1110603-rumah-cluster-pitara-kota-depok.html                                 
    500     100   70       http://rumahdijual.com/depok/1110579-rumah-cluster-pitara-kota-depok.html                                 
    500     100   70       http://rumahdijual.com/depok/1110523-rumah-cluster-pitara-kota-depok.html                                 
    500     100   70       http://rumahdijual.com/depok/1104426-hunian-cluster-depok.html                                            
    500     100   70       http://rumahdijual.com/depok/1112152-hunian-cluster-one-gate-system-di-jalan-pitara.html                  
    500     100   70       http://rumahdijual.com/depok/1137985-rumah-cluster-banyak-tipe-depok.html                                 
    500     100   70       http://rumahdijual.com/depok/1137997-hunian-asri-minimalis-depok.html                                     
    500     100   70       http://rumahdijual.com/depok/1145555-hunian-strategis-kemana-mana-dekat.html                              
    500     100   70       http://rumahdijual.com/depok/1209195-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html         
    500     100   70       http://rumahdijual.com/depok/1209087-iklan-foto-asli.html                                                 
    500     100   70       http://rumahdijual.com/depok/1208901-rumah-luas-harga-luas-depok.html                                     
    500     100   70       http://rumahdijual.com/depok/1207444-cluster-banyak-pilihan-depok.html                                    
    500     100   70       http://rumahdijual.com/depok/1207442-cluster-banyak-pilihan-depok.html                                    
    500     100   70       http://rumahdijual.com/depok/1207191-rumah-dalam-cluster-one-gate-system.html                             
    500     100   70       http://rumahdijual.com/depok/1191951-rumah-luas-harga-murah-di-pitara-depok.html                          
    500     100   70       http://rumahdijual.com/depok/1191949-rumah-cluster-one-gate-system.html                                   
    500     100   70       http://rumahdijual.com/depok/1177139-rumah-baru-ready-dan-indet-pitara-depok.html                         
    500     100   70       http://rumahdijual.com/depok/1175009-rumah-adem-harga-tentrem.html                                        
    500     100   70       http://rumahdijual.com/depok/1175000-hunian-di-lokasi-strategis-pitara-depok.html                         
    500     100   70       http://rumahdijual.com/depok/1150849-hunian-luas-harga-murah-depok.html                                   
    500     100   70       http://rumahdijual.com/depok/1150833-rumah-cluster-di-pitara-depok.html                                   
    500     100   70       http://rumahdijual.com/depok/1150832-hunian-strategis-cocok-unt-invest.html                               
    500     100   70       http://rumahdijual.com/depok/1145594-hunian-harga-murah-pitara-depok.html                                 
    500     100   70       http://rumahdijual.com/depok/1103839-rumah-cluster-one-gate-system.html                                   
    500     100   70       http://rumahdijual.com/depok/1102323-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html          
    500     100   70       http://rumahdijual.com/depok/1063752-rumah-cluster-di-pitara-kota-depok-strategis.html                    
    500     100   70       http://rumahdijual.com/depok/1058839-rumah-15-menit-ke-pusat-kota-depok.html                              
    500     100   70       http://rumahdijual.com/depok/1209407-rumah-cluster-di-pitara-kota-depok-strategis.html                    
    500     100   70       http://rumahdijual.com/depok/1056761-rumah-cluster-pitara-kota-depok.html                                 
    500     100   70       http://rumahdijual.com/depok/1222593-griya-pratama-asri-siap-huni.html                                    
    500     100   70       http://rumahdijual.com/depok/1229175-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html          
    500     100   70       http://rumahdijual.com/depok/1229258-rumah-cluster-pitara-kota-depok.html                                 
    500     100   70       http://rumahdijual.com/depok/1182896-rumah-cluster-one-gate-system-ready-stock.html                       
    500     100   70       http://rumahdijual.com/depok/1145611-rumah-manis-minimalis-dan-strategis-depok.html                       
    500     100   70       http://rumahdijual.com/depok/1128317-rumah-baru-harga-seru-pitara-kota-depok.html                         
    500     100   70       http://rumahdijual.com/depok/1244205-hunian-cluster-di-pitara-kota-depok-lantai-full-granit.html          
    500     100   70       http://rumahdijual.com/depok/1244195-griya-pratama-asri-siap-huni.html                                    
    500     100   70       http://rumahdijual.com/depok/1238260-rumah-cluster-pitara.html                                            
    500     100   70       http://rumahdijual.com/depok/1233760-hunian-cluster-di-pitara-kota-depok-lantai-full-granit.html          
    500     100   70       http://rumahdijual.com/depok/1229279-hunian-cluster-di-pitara-kota-depok-lantai-full-granite.html         
    500     100   70       http://rumahdijual.com/depok/1078510-rumah-dekat-jalan-villa-santika.html                                 
    500     100   70       http://rumahdijual.com/depok/1298549-rumah-cluster-pitara-pancoran-mas-kota-depok.html                    
    500     100   70       http://rumahdijual.com/depok/1293541-rumah-strategis-keamanan-24jam-di-pitara-depok.html                  
    500     100   70       http://rumahdijual.com/depok/1270942-rumah-siap-huni-dan-bersertifikat-di-pitara-depok.html               
    500     100   70       http://rumahdijual.com/depok/1243169-griya-pratama-asri-siap-huni.html                                    
    500     100   70       http://rumahdijual.com/depok/1232231-rumah-kota-depok.html                                                
    500     100   65       http://rumahdijual.com/depok/980977-rumah-mini-cluster-cipayung-depok.html                                
    500     100   65       http://rumahdijual.com/depok/1242590-rumah-minimalis-dekat-pusat-kota.html                                
    500     100   65       http://rumahdijual.com/depok/1242584-rumah-minimalis-nempel-perumahan-permata-regency-kota-depok.html     
    500     100   65       http://rumahdijual.com/depok/1242539-rumah-minimalis-nempel-perumahan-permata-regency-kota-depok.html     
    500     100   65       http://rumahdijual.com/depok/1239879-cluster-elit-harga-irit.html                                         
    500     100   65       http://rumahdijual.com/depok/1228396-rumah-cluster-nempel-permata-regency.html                            
    500     100   65       http://rumahdijual.com/depok/1209422-rumah-cluster-di-lokasi-strategis-depok.html                         
    500     100   65       http://rumahdijual.com/depok/1209389-rumah-cluster-pitara-kota-depok.html                                 
    500     100   65       http://rumahdijual.com/depok/1100084-rumah-cluster-pancoran-mas-depok.html                                
    500     100   65       http://rumahdijual.com/depok/1099796-rumah-cluster-di-lokasi-strategis-pitara-kota-depok.html             
    500     100   65       http://rumahdijual.com/depok/1099761-cluster-pitara-kec-pancoran-mas-depok.html                           
    500     100   65       http://rumahdijual.com/depok/1095142-rumah-cluster-kemna-mana-dekat.html                                  
    500     100   65       http://rumahdijual.com/depok/1094207-rumah-cluster-ga-cuma-1-type.html                                    
    500     100   65       http://rumahdijual.com/depok/1094197-rumah-cluster-pitara-depok.html                                      
    500     100   60       http://rumahdijual.com/depok/1102132-rumah-cluster-siap-huni-kota-depok.html                              
    500     100   60       http://rumahdijual.com/depok/1101870-rumah-murah-kemana2-cuma-selangkah.html                              
    500     100   60       http://rumahdijual.com/depok/1089424-cluster-permata-dekat-dengan-stasiun.html                            
    500     100   60       http://rumahdijual.com/depok/1078891-rumah-cluster-pancoran-mas-depok-pitara.html                         
    500     100   60       http://rumahdijual.com/depok/1061542-hunian-3-kamar-lantai-full-granite.html                              
    500     100   60       http://rumahdijual.com/depok/1060655-rumah-cluster-kota-depok.html                                        
    500     100   60       http://rumahdijual.com/depok/1060639-mau-punya-rumah-mewah-harga-dibawah-700-juta-yuk.html                
    500     100   60       http://rumahdijual.com/depok/976329-cari-rumah-nih-tips-nya-hehe.html                                     
    500     100   60       http://rumahdijual.com/depok/1102159-rumah-cluster-pancoran-mas-depok-jalan-raya-pitara.html              
    500     100   60       http://rumahdijual.com/depok/1224578-rumah-minimalis-dekat-kemana-mana.html                               
    500     100   60       http://rumahdijual.com/depok/984827-rumah-murah-kemana2-cuma-selangkah.html                               
    500     100   60       http://rumahdijual.com/depok/1242517-sebut-saja-rumah-cluster-kota-depok.html                             
    500     100   160      http://rumahdijual.com/depok/1000271-rumah-2-lantai-di-harjamukti-cimanggis-depok.html                    
    500     100   140      http://rumahdijual.com/depok/1114888-rumah-murah-depok.html                                               
    500     100   100      http://rumahdijual.com/depok/1033544-rumah-dua-lantai-komplek-gobel-mekarsari-depok-bisa-kpr.html
    


```python
selectExpensive(df, avg, unit)
```

    
    EXPENSIVE PRICE
    -----------------
    is when the price is above average: 454 (million IDR) but you only get land below average: 88 (square meters) and building below average: 55 (square meters).
    
    
    
    There are : 323  items that matched the EXPENSIVE category.
    
    price land building                                                                                                         url
    455     84   45       http://rumahdijual.com/depok/829084-rumah-cluster-mampang-2-bisa-kpr.html                                
    455     84   45       http://rumahdijual.com/depok/835769-mampang-indah-2-depok.html                                           
    455     84   45       http://rumahdijual.com/depok/828862-rumah-murah-pancoran-mas-bisa-kpr.html                               
    455     78   50       http://rumahdijual.com/depok/1029716-rumah-di-grand-depok-city.html                                      
    455     78   50       http://rumahdijual.com/depok/972641-rumah-mungil-di-grand-depok-city.html                                
    455     77   40       http://rumahdijual.com/depok/1203083-di-jual-rumah-cipta-kalimulya-residence.html                        
    455     72   45       http://rumahdijual.com/depok/1144223-spek-super-20m-ke-jl-raya.html                                      
    455     71   36       http://rumahdijual.com/depok/1121866-rumah-baru-tipe-36-71-kpr-rp-455jt-di.html                          
    456     84   45       http://rumahdijual.com/depok/828854-dijual-rumah-murah-di-mampang-depok.html                             
    456     82   50       http://rumahdijual.com/depok/841243-cluster-kota-harga-desa.html                                         
    456     82   40       http://rumahdijual.com/depok/1310565-cluster-selangkah-menuju-stasiun-depok.html                         
    456     79   45       http://rumahdijual.com/depok/1265870-rumah-400-jtan-depok-ready.html                                     
    456     72   36       http://rumahdijual.com/depok/1274244-cari-rumah-di-depok-sawangan-di-jalan-jabon-bisa.html               
    456     72   36       http://rumahdijual.com/depok/1274225-rumah-dijual-di-sawangan-di-jalan-pengasinan-bojongsari-depok.html  
    456     72   36       http://rumahdijual.com/depok/1256131-rumah-dijual-depok-di-bojongsari-investasi-properti-terbaik.html    
    456     72   36       http://rumahdijual.com/depok/1256121-iklan-rumah-dijual-depok-dijual-rumah-depok-di-bojongsari.html      
    456     72   36       http://rumahdijual.com/depok/1256118-info-rumah-dijual-murah-di-depok-dijual-rumah-bojongsari.html       
    456     72   36       http://rumahdijual.com/depok/1256108-dijual-cepat-rumah-jl-bojongsari-depok-aman-dan-strategis.html      
    456     72   36       http://rumahdijual.com/depok/1256133-rumah-dijual-depok-di-bojongsari-2016-hari-ini.html                 
    456     30   35       http://rumahdijual.com/depok/1210948-rumah-murah-dan-cantik-dmarco-di-cilodong-depok.html                
    457     82   44       http://rumahdijual.com/depok/783864-cipayung-royal-residence-hadir-untuk-anda.html                       
    457     75   45       http://rumahdijual.com/depok/1109404-perumahan-asri-jayana-villas-cibinong-dekat-pemda-bogor.html        
    458     84   38       http://rumahdijual.com/depok/939143-perumahan-cantik-depok-r21-0272-a.html                               
    458     84   38       http://rumahdijual.com/depok/920251-cluster-amaryllis-di-abdul-gani-kalibaru-depok-r21-0272-a.html       
    458     72   44       http://rumahdijual.com/depok/914497-rumah-baru-di-belakang-gdc-bia-kpr-tanpa-ke.html                     
    459     78   40       http://rumahdijual.com/depok/1205260-dijual-rumah-dikalimulya-cilodong-depok.html                        
    459     72   50       http://rumahdijual.com/depok/1124262-jual-cepat-rumah-dalam-kompleks-full-renov-tinggal-ngepel.html      
    459     72   50       http://rumahdijual.com/depok/1259393-rumah-murah-fasilitas-bintang-lima-lokasi-superstrategis.html       
    459     72   50       http://rumahdijual.com/depok/1238034-rumah-elit-banting-harga-free-bphtn-dan-ajb.html                    
    459     72   50       http://rumahdijual.com/depok/1233043-rumah-keren-banting-harga-di-perum-taman-anyelir-3-a.html           
    459     72   50       http://rumahdijual.com/depok/1040972-rumah-murah-fasad-minimalis-modern-di-grand-depok-city.html         
    459     72   30       http://rumahdijual.com/depok/968648-permata-cimanggis-depok.html                                         
    459     72   30       http://rumahdijual.com/depok/903862-permata-cimanggis-depok.html                                         
    459     72   30       http://rumahdijual.com/depok/1031904-permata-cimanggis-cluster-jamrud.html                               
    459     72   30       http://rumahdijual.com/depok/970344-cluster-jamrud-di-permata-cimanggis.html                             
    460     81   45       http://rumahdijual.com/depok/1277760-rumah-minimalis-dicluster-kampung-pedati-2-depok.html               
    460     81   40       http://rumahdijual.com/depok/1136580-rumah-di-depok-murah.html                                           
    460     80   45       http://rumahdijual.com/depok/1245850-rumah-murah-di-depok-lokasi-strategis.html                          
    460     78   39       http://rumahdijual.com/depok/1266387-cluster-terbaru-di-depok-akses-jl-raya-bogor-design.html            
    460     77   50       http://rumahdijual.com/depok/970494-town-house-di-area-grand-depok-city-sp-189-a.html                    
    460     73   45       http://rumahdijual.com/depok/1073915-di-jual-3-unit-kavling-siap-bangun.html                             
    460     73   45       http://rumahdijual.com/depok/1059546-di-jual-rumah-baru-di-depok.html                                    
    460     73   43       http://rumahdijual.com/depok/848920-rumah-murah-di-depok.html                                            
    460     72   48       http://rumahdijual.com/depok/948361-rumah-minimalis-permata-regency.html                                 
    460     72   45       http://rumahdijual.com/depok/1268295-rumah-baru-dekat-sekolah-global-islamic-dan-rs-citra.html           
    460     72   39       http://rumahdijual.com/depok/1291016-cluster-gress-di-depok-promo-unit-perdana-design-dijamin.html       
    460     72   39       http://rumahdijual.com/depok/1295556-jayana-valley-harga-promo-unit-perdana-banyak-discountnya.html      
    460     65   45       http://rumahdijual.com/depok/822160-rumah-murah-cluster-tanah-baru-depok-120-m-dr.html                   
    460     60   45       http://rumahdijual.com/depok/1139033-rumah-baru-nyaman-cluster-di-tanah-baru-dekat-angkot.html           
    460     56   50       http://rumahdijual.com/depok/1260393-rumah-10-menit-ke-stasiun-depok-lama.html                           
    461     85   45       http://rumahdijual.com/depok/840048-cluster-siap-huni-bumi-mekar-kencana-cilodong.html                   
    461     75   36       http://rumahdijual.com/depok/1141355-cluster-sawangan-gardenia.html                                      
    462     84   48       http://rumahdijual.com/depok/875064-rumah-baru-dalam-cluster-di-depok.html                               
    462     84   40       http://rumahdijual.com/depok/1294299-beli-rumah-free-biaya-biaya-diskon-15-juta-di.html                  
    462     84   40       http://rumahdijual.com/depok/1297303-rumah-gratis-biaya-biaya-diskon-15-jt-di-grand.html                 
    462     84   40       http://rumahdijual.com/depok/1295332-rumah-gratis-biaya-biaya-diskon-15-jt-di-grand.html                 
    462     84   40       http://rumahdijual.com/depok/1291895-cluster-free-biaya-biaya-di-grand-depok-city.html                   
    462     84   40       http://rumahdijual.com/depok/1260233-cluster-murah-di-depok.html                                         
    462     83   48       http://rumahdijual.com/depok/874487-rumah-dijual-daerah-cilodong-depok.html                              
    462     83   48       http://rumahdijual.com/depok/875091-jual-rumah-cilodong-depok.html                                       
    462     83   48       http://rumahdijual.com/depok/874946-rumah-dijual-di-daerah-cilodong-depok.html                           
    462     83   48       http://rumahdijual.com/depok/874492-rumah-dijual-di-daerah-cilodong-depok.html                           
    462     83   48       http://rumahdijual.com/depok/872575-rumah-murah-di-di-depok.html                                         
    464     84   45       http://rumahdijual.com/depok/767535-hunian-asri-nan-strategis-dekat-dengan-jalan-raya-diskon.html        
    465     84   36       http://rumahdijual.com/depok/890005-rumah-dijual-type-36-84-a.html                                       
    465     84   36       http://rumahdijual.com/depok/576721-rumah-minilmalis-dijual-lokasi-strategis.html                        
    465     81   48       http://rumahdijual.com/depok/961674-rumah-halus-mulus-ready-akses-bagus-di-pancoran-mas.html             
    465     80   41       http://rumahdijual.com/depok/1037975-rumah-minimalis-di-kalimulya-depok.html                             
    465     74   50       http://rumahdijual.com/depok/581801-perumahan-nur-az-residnce-sukatani-cimanggis.html                    
    465     70   45       http://rumahdijual.com/depok/1295076-rumah-tanpa-dp-di-depok.html                                        
    467     87   48       http://rumahdijual.com/depok/840058-cluster-ready-stock-bumi-mekar-kencana-cilodong.html                 
    467     81   39       http://rumahdijual.com/depok/1208397-perumahan-type-39-115-a.html                                        
    467     72   39       http://rumahdijual.com/depok/1305138-rumah-tinggal-ternyaman-di-depok-lingkungan-asri-dan-design.html    
    468     84   36       http://rumahdijual.com/depok/931836-arco-residence.html                                                  
    468     75   39       http://rumahdijual.com/depok/1266483-hunian-terbaru-di-tapos-depok-lokasi-berkembang-dan-design.html     
    468     72   39       http://rumahdijual.com/depok/1294123-jual-rumah-baru-jayana-valley-depok-jatijajar-jawa-barat.html       
    468     72   39       http://rumahdijual.com/depok/1311419-perumahan-dengan-konsep-modern-di-dataran-lembah-yg-asri.html       
    468     72   39       http://rumahdijual.com/depok/1302828-rumah-baru-type-minimalis-modern-jayana-valley-depok.html           
    468     72   39       http://rumahdijual.com/depok/1291459-beli-rumah-bisa-umroh-tanpa-di-undi-untuk-5-a.html                  
    468     72   39       http://rumahdijual.com/depok/1255834-perumahan-mewah-cocok-untuk-rumah-tinggal-maupun-investasi-di.html  
    468     72   39       http://rumahdijual.com/depok/1290386-rumah-baru-bisa-kpr-cash-bertahap-cash-keras-hanya.html             
    468     72   39       http://rumahdijual.com/depok/1288196-rumah-cluster-yang-mewah.html                                       
    468     72   39       http://rumahdijual.com/depok/1288064-rumah-impian-jayana-valley.html                                     
    468     72   39       http://rumahdijual.com/depok/1268415-rumah-cluster-jayana-valley.html                                    
    468     72   39       http://rumahdijual.com/depok/1267180-perumahan-jayana-valley-di-depok-jatijajar.html                     
    468     72   39       http://rumahdijual.com/depok/1255814-jayana-valley-investasi-mewah-nan-terjangkau.html                   
    468     72   39       http://rumahdijual.com/depok/1291339-cluster-modern-kualitas-bangunan-terbaik-harga-ciamik.html          
    469     77   36       http://rumahdijual.com/depok/913230-rumah-asri-murah-di-grand-depok-city.html                            
    470     86   45       http://rumahdijual.com/depok/655079-griya-alphari-town-house-eksklusif-di-depok-harga-400-a.html         
    470     81   50       http://rumahdijual.com/depok/431345-rumah-dp-suka-suka-di-pamulang.html                                  
    470     80   42       http://rumahdijual.com/depok/1212652-dijual-rumah-murah-di-depok-akses-strategis.html                    
    470     80   42       http://rumahdijual.com/depok/1200980-rumah-murah-harga-karyawan-lokasi-pinggir-jalan.html                
    470     80   42       http://rumahdijual.com/depok/1199930-cluster-murah-di-jalan-raya-parung-bojong-sari-pamulang.html        
    470     80   42       http://rumahdijual.com/depok/1196849-dijual-perumahan-termurah-dan-terasri-didaerah-depok.html           
    470     80   42       http://rumahdijual.com/depok/1191921-perumahan-murah-di-bojong-sari-depok.html                           
    470     80   42       http://rumahdijual.com/depok/1194111-rumah-di-jual-di-depok.html                                         
    470     80   42       http://rumahdijual.com/depok/1193694-rumah-siap-huni-dalam-perumahan-di-bojongsari-ciputat-depok.html    
    470     80   42       http://rumahdijual.com/depok/1243227-cluster-bojong-sari-depok.html                                      
    470     80   42       http://rumahdijual.com/depok/1191711-rumah-murah-dan-strategis-di-bojongsari-depok.html                  
    470     80   42       http://rumahdijual.com/depok/1190567-cluster-murah-dan-strategis-di-bojongsari-depok.html                
    470     80   42       http://rumahdijual.com/depok/1196182-cluster-murah-dan-strategis-di-bojongsari-depok.html                
    470     80   42       http://rumahdijual.com/depok/1257849-cluster-strategis-di-depok.html                                     
    470     80   42       http://rumahdijual.com/depok/1312566-perumahan-di-bojong-sari-promo-sampai-akhir-maret.html              
    470     80   42       http://rumahdijual.com/depok/1189800-di-jual-rumah-cluster-pinggir-jalan-raya-ciputat-parung.html        
    470     80   42       http://rumahdijual.com/depok/1290300-cluster-murah-dan-strategis-di-pinggir-jalan-ciputat-parung.html    
    470     80   42       http://rumahdijual.com/depok/1186229-harga-promo-cluster-di-pinggir-jalan-raya-ciputat-parung.html       
    470     78   39       http://rumahdijual.com/depok/1073719-rumah-murah-di-gdc-depok-di-kavling-kemang.html                     
    470     77   36       http://rumahdijual.com/depok/979885-rumah-asri-murah-di-grand-depok-city.html                            
    470     77   36       http://rumahdijual.com/depok/1019543-best-price-rumah-asri-murah-di-grand-depok-city.html                
    470     76   40       http://rumahdijual.com/depok/1133862-rumah-mampang-indah-2-a.html                                        
    470     72   54       http://rumahdijual.com/depok/1306576-rumah-hook-siap-huni-harga-dibawah-pasaran-tanah-baru.html          
    472     75   47       http://rumahdijual.com/depok/590297-perumahan-muslim-murah-di-sawangan-depok.html                        
    475     81   40       http://rumahdijual.com/depok/1169396-2-unit-lagi-segera-atau-tidak-sama-sekali.html                      
    475     80   45       http://rumahdijual.com/depok/1110621-rumah-baru-dijual-cluster-di-grogol-limo-depok.html                 
    475     79   54       http://rumahdijual.com/depok/1213365-rumah-baru-dan-murah-sarana-terjangkau.html                         
    475     78   52       http://rumahdijual.com/depok/1031196-rumah-cantik-di-samping-dtc-pancoran-mas-depok.html                 
    475     78   45       http://rumahdijual.com/depok/1263288-cluster-asri-siap-huni-di-grand-depok-city-r21.html                 
    475     78   36       http://rumahdijual.com/depok/876365-perumahan-cluster-di-grand-depok-city-murah-strategis.html           
    475     78   36       http://rumahdijual.com/depok/861340-grand-dahlia-cluster-depok.html                                      
    475     78   36       http://rumahdijual.com/depok/841546-grand-cluster-dahlia-hunian-cantik-asri-di-kota-depok.html           
    475     72   54       http://rumahdijual.com/depok/1295727-di-jual-rumah-minimalis-di-pondok-petir-sawangan.html               
    475     72   50       http://rumahdijual.com/depok/908369-rumah-baru-di-renovasi-di-cinere-depok.html                          
    475     72   45       http://rumahdijual.com/depok/1026036-rumah-murah-di-permata-cimanggis-depok.html                         
    475     72   45       http://rumahdijual.com/depok/1024832-di-jual-rumah-lokasi-strategis-di-sukmajaya.html                    
    475     72   38       http://rumahdijual.com/depok/963435-perumahan-berbukit-disawangan-depok.html                             
    475     72   38       http://rumahdijual.com/depok/1036195-perumahan-tanpa-dp-didepok.html                                     
    475     72   38       http://rumahdijual.com/depok/1036087-perumahan-berbukit-disawangan-depok.html                            
    475     72   36       http://rumahdijual.com/depok/1013987-rumah-baru-ready-stock-di-area-gdc-depok.html                       
    475     72   36       http://rumahdijual.com/depok/1013257-rumah-di-cluster-dekat-grand-depok-city.html                        
    475     70   45       http://rumahdijual.com/depok/1246223-rumah-hook-bisa-kpr-berada-di-dalam-perumahan-mampang.html          
    475     70   45       http://rumahdijual.com/depok/1103914-cluster-murah-di-bedahan-tugu-sawangan-depok.html                   
    475     70   45       http://rumahdijual.com/depok/1097639-rumah-sederhana-harga-impian-di-depok.html                          
    475     70   45       http://rumahdijual.com/depok/1103976-cluster-cantik-dan-nyaman-di-sawangan-depok.html                    
    476     72   30       http://rumahdijual.com/depok/682735-rumah-di-depok-30-72-safir-jamrud-permata-cimanggis.html             
    476     72   30       http://rumahdijual.com/depok/1227127-rumah-murah-cluster-jamrud-di-permata-cimanggis-depok.html          
    476     72   30       http://rumahdijual.com/depok/1024781-rumah-mewah-murah-cluster-di-permata-cimanggis-depok-free.html      
    476     72   30       http://rumahdijual.com/depok/1012511-rumah-minimalis-murah-strategis-depok-free-biaya2.html              
    476     6    30       http://rumahdijual.com/depok/596384-permata-cimanggis-depok.html                                         
    477     81   42       http://rumahdijual.com/depok/1206198-dijual-rumah-dikalimulya-dekat-kota-kembang.html                    
    478     78   36       http://rumahdijual.com/depok/1122248-rumah-cluster-grand-depok-city-tahap-2-di-depok.html                
    478     78   36       http://rumahdijual.com/depok/835356-cluster-andalan-grand-dahlia-depok-ready-stock.html                  
    478     72   38       http://rumahdijual.com/depok/1065626-jual-rumah-exclusive-sawangan-depok.html                            
    478     72   38       http://rumahdijual.com/depok/622307-perumahan-asri-dan-nyaman-di-pesona-sawangan-residence.html          
    479     70   45       http://rumahdijual.com/depok/1057100-rumah-dekat-gdc-bisa-kpr-tanpa-denda-dan-atau.html                  
    480     86   45       http://rumahdijual.com/depok/1238700-dijual-rumah-di-perumahan-sawangan-hill-jl-curug-raya.html          
    480     84   45       http://rumahdijual.com/depok/1002583-mau-rumah-dp-48-juta-sawangan-depok.html                            
    480     84   45       http://rumahdijual.com/depok/1163444-perumahan-depok-country-dp-7-5juta-langsung-shm.html                
    480     84   45       http://rumahdijual.com/depok/734991-rumah-murah-depok.html                                               
    480     82   50       http://rumahdijual.com/depok/988340-cluster-murah-sejuk-nyaman-asri-strategis-asri-cagar-alam.html       
    480     79   45       http://rumahdijual.com/depok/1263817-siap-huni.html                                                      
    480     79   45       http://rumahdijual.com/depok/1265143-rumah-siap-huni.html                                                
    480     79   45       http://rumahdijual.com/depok/1280628-rumah-ready-stock-lokasi-mampang-depok.html                         
    480     77   45       http://rumahdijual.com/depok/603974-cluster-bale-pancoran-mas-depok.html                                 
    480     75   48       http://rumahdijual.com/depok/943692-rumah-asri-dan-nyaman-harga-gak-masalah-kawasan-cimanggis.html       
    480     75   45       http://rumahdijual.com/depok/1301558-dijual-rumah-baru-di-cinere-depok-sawangan.html                     
    480     75   45       http://rumahdijual.com/depok/1134684-rumah-murah-depok-bedahan.html                                      
    480     74   45       http://rumahdijual.com/depok/1257100-dlt-lavender-depok-cash-atau-kpr.html                               
    480     74   45       http://rumahdijual.com/depok/1257075-dlt-lavender-depok.html                                             
    480     72   48       http://rumahdijual.com/depok/983167-permata-depok-regency.html                                           
    480     72   46       http://rumahdijual.com/depok/887089-rumah-baru-di-teratai-residence-cilodong-depok-harga-400-a.html      
    480     72   39       http://rumahdijual.com/depok/1235505-new-hot-promo-perumahan-eksklusif-depok-jayana-valley.html          
    480     70   45       http://rumahdijual.com/depok/1136418-rumah-cluster-murah-dp-suka-suka.html                               
    480     70   45       http://rumahdijual.com/depok/1115197-cluster-di-depok-bebas-biaya-kpr-dan-bphtb.html                     
    480     70   45       http://rumahdijual.com/depok/1114922-bedahan-tugu-rumah-murah-di-daerah-depok.html                       
    480     70   45       http://rumahdijual.com/depok/1114235-rumah-murah-di-depok-dengan-diskon-10-untuk-promo.html              
    480     70   45       http://rumahdijual.com/depok/1114226-rumah-baru-di-depok-400-jutaan-bebas-biaya-kpr.html                 
    480     70   45       http://rumahdijual.com/depok/1114830-rumah-baru-murah-dalam-cluster-modern-di-depok.html                 
    480     70   45       http://rumahdijual.com/depok/1110966-rumah-cantik-di-bedahan-tugu-depok.html                             
    480     70   45       http://rumahdijual.com/depok/1108604-cluster-murah-di-daerah-depok-400-juta.html                         
    480     70   45       http://rumahdijual.com/depok/1108047-cluster-murah-dp-ringan-bedahan-tugu-depok.html                     
    480     70   45       http://rumahdijual.com/depok/1107908-rumah-murah-di-depok-dp-suka-suka-bedahan.html                      
    480     70   45       http://rumahdijual.com/depok/1112638-rumah-400-jutaan-dekat-akses-tol-cijago.html                        
    480     70   36       http://rumahdijual.com/depok/1306779-rumah-minimalis-di-tanah-baru-depok.html                            
    480     70   36       http://rumahdijual.com/depok/1273265-rumah-modern-desain-cantik-di-tanah-baru-depok.html                 
    483     75   36       http://rumahdijual.com/depok/1294382-grand-dahlia-cluster-tahap-iii.html                                 
    483     72   36       http://rumahdijual.com/depok/1295567-rumah-di-gdc-ada-kolam-renang-dp-bisa-dicicil.html                  
    484     84   38       http://rumahdijual.com/depok/483190-new-poin-mas-depok.html                                              
    485     87   36       http://rumahdijual.com/depok/918335-cluster-esklusif-di-depok-timur.html                                 
    485     85   45       http://rumahdijual.com/depok/903919-rumah-minimalis-di-cilodong-harga-terjangkau-promo-dp-suka.html      
    485     85   45       http://rumahdijual.com/depok/906626-rumah-baru-di-cilodong-promo-akhir-tahun-dp-suka.html                
    485     82   54       http://rumahdijual.com/depok/1165705-rumah-second-type-54-82-di-mampamg-depok.html                       
    485     78   36       http://rumahdijual.com/depok/815453-rumah-baru-dekat-gdc-dan-stasiun-depok-lama.html                     
    485     78   36       http://rumahdijual.com/depok/896412-rumah-cluster-murah-di-kawasan-gdc-depok.html                        
    485     77   42       http://rumahdijual.com/depok/1156573-dijual-rumah-baru-renvasi-minimalis-modern-lokasi-di-cimanggis.html 
    485     72   46       http://rumahdijual.com/depok/783657-di-jual-rumah-baru-di-perumahan-raden-saleh-depok.html               
    485     72   36       http://rumahdijual.com/depok/949879-hah-dp-hanya-20jt-bisa-dapet-rumah-cluster-di.html                   
    485     72   36       http://rumahdijual.com/depok/873629-segera-sebelum-kehabisan-dp-ringan-bs-dicicil-bonus-kitchen.html     
    485     72   36       http://rumahdijual.com/depok/809292-cluster-lavinia-residence-lokasi-mampang-depok.html                  
    485     72   36       http://rumahdijual.com/depok/1227492-cluster-lavinia-hunian-nyaman-harga-teman-dp-ringan.html            
    485     72   36       http://rumahdijual.com/depok/797706-cluster-minimalis-harga-ekomonis-mampang-depok.html                  
    485     72   36       http://rumahdijual.com/depok/800395-cluster-minimalis-lokasi-strategis.html                              
    485     72   36       http://rumahdijual.com/depok/1021160-cluster-lavinia-residence-36-unit-lokasi-dekat-mall-dtc.html        
    485     72   36       http://rumahdijual.com/depok/1077729-cluster-lavinia-residence.html                                      
    485     72   36       http://rumahdijual.com/depok/1193038-cluster-lavinia-residence-hunian-cantik-lokasi-apik.html            
    485     72   36       http://rumahdijual.com/depok/1194608-cluster-lavinia-residence-spek-boleh-diadu.html                     
    485     72   36       http://rumahdijual.com/depok/1225144-cluster-lavinia-residence-lokasi-sip-spek-boleh-di-adu.html         
    485     72   36       http://rumahdijual.com/depok/350137-town-house-lavinia-residence-depok-ready-stock-free-biaya.html       
    485     56   54       http://rumahdijual.com/depok/968744-di-jual-rumah-baru-nempel-gdc-model-town-house.html                  
    487     73   46       http://rumahdijual.com/depok/721790-dapatkan-fasilitas-bonus-rumah-pantas-unit-terbatas-studio-alam.html 
    488     76   36       http://rumahdijual.com/depok/1314347-cluster-di-grand-depok-city-pembukaan-tahap-3-lokasi.html           
    488     76   36       http://rumahdijual.com/depok/1312729-perumahan-di-grand-depok-city-pembukaan-tahap.html                  
    488     76   36       http://rumahdijual.com/depok/1313194-rumah-murah-di-grand-depok-city-dp-48-jt.html                       
    488     76   36       http://rumahdijual.com/depok/1310764-perumahan-grand-depok-city-harga-488-jt-akan-naik.html              
    488     76   36       http://rumahdijual.com/depok/1312479-cluster-di-grand-depok-city-pembukaan-tahap-3-promo.html            
    490     85   46       http://rumahdijual.com/depok/1265724-rumah-baru-murah-di-cilodong.html                                   
    490     84   41       http://rumahdijual.com/depok/909039-rumah-cantik-semi-furnished-di-depok.html                            
    490     80   54       http://rumahdijual.com/depok/1261143-cluster-villa-sawangan-depok.html                                   
    490     78   45       http://rumahdijual.com/depok/1047613-rumah-mungil-di-perumahan-besar-tanah-baru-harga-bawah.html         
    490     78   45       http://rumahdijual.com/depok/860420-rumah-mungil-di-perumahan-besar-tanah-baru-harga-bawah.html          
    490     77   45       http://rumahdijual.com/depok/739073-cluster-lavinia-residence-depok.html                                 
    490     76   39       http://rumahdijual.com/depok/1270855-hunian-paling-unik-di-depok-harga-terjangkau-di-lokasi.html         
    490     75   40       http://rumahdijual.com/depok/1258502-rumah-baru-nyaman-di-kelapa-dua-depok-490-jt.html                   
    490     74   50       http://rumahdijual.com/depok/1274734-cepaaat-rumah-dijual-murah-di-kalimulya-depok.html                  
    490     72   45       http://rumahdijual.com/depok/836885-jual-rumah-perum-permata-cimanggis-depok-bisa-kpr.html               
    490     72   36       http://rumahdijual.com/depok/1306759-rumah-minimalis-tanah-baru-depok.html                               
    490     72   30       http://rumahdijual.com/depok/440080-dijual-rumah-300jtan-di-depok-permata-cimanggis.html                 
    490     70   50       http://rumahdijual.com/depok/1131155-new-cluster-depok-2-tengah-15-mnt-ke-stasiun.html                   
    490     70   45       http://rumahdijual.com/depok/1266956-claster-siap-huni-rangkapan-jaya.html                               
    490     7    45       http://rumahdijual.com/depok/1314443-perumahan-sederhana-di-depok-0813-1048-0064-a.html                  
    490     61   45       http://rumahdijual.com/depok/1158402-rumah-murah-cluster-120-m-dr-angkot-d-105-a.html                    
    490     61   45       http://rumahdijual.com/depok/898894-rumah-murah-unit-terakhir-cluster-120-m-dr-angkot.html               
    491     84   36       http://rumahdijual.com/depok/1204461-rumah-minimalis-lokasi-strategis.html                               
    491     70   45       http://rumahdijual.com/depok/860958-perumahan-baru-pancoran-indah-mampang-depok.html                     
    491     70   45       http://rumahdijual.com/depok/895664-rumah-tanpa-dp-pancoran-indah-residence.html                         
    492     72   50       http://rumahdijual.com/depok/1004538-67-hunian-bagus-cantik-siap-huni-di-permata-depok.html              
    492     72   40       http://rumahdijual.com/depok/925880-rumah-cluster-di-kota-depok.html                                     
    493     78   39       http://rumahdijual.com/depok/1280598-96-unit-ekslusif-harga-perdana-banyak-promo-di-jayana.html          
    495     84   36       http://rumahdijual.com/depok/1115208-rumah-bagus-free-semua-biaya-dp-suka-suka-dekat.html                
    495     84   36       http://rumahdijual.com/depok/1115335-rumah-nyaman-free-all-dp-ringan-dekat-tol-dan.html                  
    495     84   36       http://rumahdijual.com/depok/1292444-rumah-murah-free-semua-biaya-bisa-tanpa-dp-5-a.html                 
    495     84   36       http://rumahdijual.com/depok/905359-rumah-nyaman-strategis-dekat-tol-jagorawi.html                       
    495     84   36       http://rumahdijual.com/depok/900020-rumah-elite-harga-irit-nyaman-strategis-dekat-tol-jagorawi.html      
    495     74   45       http://rumahdijual.com/depok/1090009-cluster-5-unit-tahap-pembangunan-belakang-grand-depok-city.html     
    495     72   45       http://rumahdijual.com/depok/1199728-rumah-minimalis-daerah-grand-depok-city.html                        
    495     72   38       http://rumahdijual.com/depok/862771-rumah-murah-lantai-dua-di-bambu-asri-depok.html                      
    495     72   38       http://rumahdijual.com/depok/428558-rumah-puri-nusa-serua-aman-nyaman-dan-asri.html                      
    495     72   36       http://rumahdijual.com/depok/963444-perumahan-dekat-dengan-dtc-depok.html                                
    495     71   46       http://rumahdijual.com/depok/991081-rumah-murah-di-dalam-perumnas-depok-lokasi-super-strategis.html      
    495     70   45       http://rumahdijual.com/depok/1080497-rumah-cluster-design-modern-akses-dekat-ke-stasiun-depok.html       
    495     70   45       http://rumahdijual.com/depok/1143345-grand-depok-city-ready-stock.html                                   
    495     66   48       http://rumahdijual.com/depok/891372-rumah-manis-cluster-120-m-dr-angkot-d-105-a.html                     
    495     66   45       http://rumahdijual.com/depok/894111-cluster-murah-120-meter-dr-angkot-d-105-bisa.html                    
    497     78   45       http://rumahdijual.com/depok/756095-rumah-10-menit-dari-stasiun-depok-bebas-biaya-biaya.html             
    497     78   45       http://rumahdijual.com/depok/900080-griya-bukit-mas-pitara-depok.html                                    
    497     78   36       http://rumahdijual.com/depok/1230907-rumah-dijual-di-grand-depok-city-cluster-baru-dekat.html            
    497     78   36       http://rumahdijual.com/depok/1232802-rumah-cantik-menawan-500jutaan-di-gdc-depok-dp-50jt.html            
    497     78   36       http://rumahdijual.com/depok/1245489-cluster-exclusive-di-grand-depok-city.html                          
    497     78   36       http://rumahdijual.com/depok/1245932-cluster-di-depok-harga-mulai-497-jt-081225517642-a.html             
    497     78   36       http://rumahdijual.com/depok/1246005-grand-depok-city-berkonsep-modern-081225517642-a.html               
    497     78   36       http://rumahdijual.com/depok/1246013-depok-cluster-murah-dan-modern-081225517642-a.html                  
    497     78   36       http://rumahdijual.com/depok/1248712-cluster-dahlia-grand-depok-city.html                                
    497     78   36       http://rumahdijual.com/depok/827880-rumah-murah-exclusive-di-boulevard-grand-depok-city.html             
    497     78   36       http://rumahdijual.com/depok/1275810-rumah-dijual-rumah-harga-murah-dan-nyaman-di-depok.html             
    497     78   36       http://rumahdijual.com/depok/1303472-rumah-cluster-cantik-ekonomis-di-kota-mandiri-depok-grand.html      
    497     78   36       http://rumahdijual.com/depok/1309724-dijual-rumah-modern-minimalis-di-depok.html                         
    497     78   36       http://rumahdijual.com/depok/953526-cluster-termurah-di-kawasan-premium-grand-depok-city.html            
    497     78   36       http://rumahdijual.com/depok/1185631-dijual-rumah-di-depok-rp-497jt-dp-50jt-bisa.html                    
    497     78   36       http://rumahdijual.com/depok/1250570-hunian-minimalis-harga-manis-gdc-dp-hanya-50-juta.html              
    497     78   36       http://rumahdijual.com/depok/1183364-cluster-di-gdc-dp-ringan-hanya-10-50jt-bisa.html                    
    497     78   36       http://rumahdijual.com/depok/1173385-rumah-baru-di-gdc-depok.html                                        
    497     78   36       http://rumahdijual.com/depok/1119043-cluster-istimewa-dekat-boulevard-grand-depok-city-stasiun-depok.html
    497     78   36       http://rumahdijual.com/depok/1034909-rumah-di-kawasan-grand-depok-city-harga-400-jt.html                 
    497     78   36       http://rumahdijual.com/depok/1162926-cluster-baru-yang-aman-nyaman-dan-exclusive-di-grand.html           
    497     78   36       http://rumahdijual.com/depok/1165127-cluster-di-grand-depok-city-dp-10-dapat-dicicil.html                
    497     78   36       http://rumahdijual.com/depok/1179474-claster-murah-dalam-komplek-grand-depok-city.html                   
    497     78   36       http://rumahdijual.com/depok/1165259-rumah-cantik-harga-menarik.html                                     
    497     78   36       http://rumahdijual.com/depok/1167471-rumah-baru-di-grand-depok-city-tahap-2-di.html                      
    497     78   36       http://rumahdijual.com/depok/1167480-rumah-di-grand-depok-city-ada-fasilitas-kolam-renang.html           
    497     78   36       http://rumahdijual.com/depok/1167627-rumah-mewah-harga-murah-di-depok.html                               
    497     78   36       http://rumahdijual.com/depok/1167787-rumah-cluster-di-grand-depok-city-sukmajaya-depok.html              
    497     78   36       http://rumahdijual.com/depok/1172077-cluster-murah-di-gdc.html                                           
    497     78   36       http://rumahdijual.com/depok/1172383-diual-rumah-di-depok-dp-murah.html                                  
    497     78   36       http://rumahdijual.com/depok/1173332-cluster-di-gdc-depok.html                                           
    497     78   36       http://rumahdijual.com/depok/1165666-cluster-teramurah-didaerah-depok.html                               
    498     84   50       http://rumahdijual.com/depok/1233851-dp-10-juta-lokasi-di-kota-depok-15-menit.html                       
    498     78   36       http://rumahdijual.com/depok/1153279-spesial-promo-untuk-januari-di-harmony-cimanggis.html               
    499     82   45       http://rumahdijual.com/depok/1221183-rumah-minimalis-di-lokasi-strategis.html                            
    499     72   36       http://rumahdijual.com/depok/1126723-perumahan-cluster-galaksi-asri-kalimulya-dekat-gdc-depok.html       
    499     66   48       http://rumahdijual.com/depok/891374-cantik-minimalis-cluster-120-m-dr-angkot-d-105-a.html                
    500     85   45       http://rumahdijual.com/depok/1046200-rumah-murah-di-depok-3-kamar-500-jtan.html                          
    500     85   45       http://rumahdijual.com/depok/1078911-rumah-greenland-forestpark-bojongsari-sawangan-depok.html           
    500     84   54       http://rumahdijual.com/depok/914201-cinere-valley-view-cinere-limo.html                                  
    500     84   54       http://rumahdijual.com/depok/902976-free-uang-muka-cinere-valley-view-lokasi-emas.html                   
    500     84   54       http://rumahdijual.com/depok/899035-cinere-valley-view-cinere-limo.html                                  
    500     84   52       http://rumahdijual.com/depok/1249830-rumah-jatimulya-depok.html                                          
    500     84   50       http://rumahdijual.com/depok/804651-cluster-dekat-az-zikra-mampang-indah-2-a.html                        
    500     84   45       http://rumahdijual.com/depok/974020-3-unit-rumah-ready-stock-di-tanah-baru.html                          
    500     84   45       http://rumahdijual.com/depok/1184706-rumah-kalimulya-depok.html                                          
    500     81   40       http://rumahdijual.com/depok/1254367-cari-rumah-di-depok-dekat-tol-cijago-dan-stasiun.html               
    500     80   50       http://rumahdijual.com/depok/951052-duh-laris-manis-tinggal-3-unit-di-taman-bumi.html                    
    500     80   48       http://rumahdijual.com/depok/955765-aditia-residence-hunian-nyaman-lokasi-tanah-baru.html                
    500     80   45       http://rumahdijual.com/depok/1125509-hunian-cluster-100meter-dari-jalan-raya-di-pitara.html              
    500     80   45       http://rumahdijual.com/depok/861871-dijual-rumah-siap-huni-cash-tanah-baru-depok.html                    
    500     80   45       http://rumahdijual.com/depok/1306361-rumah-minimalis-murah-di-tanah-baru-beji-depok.html                 
    500     80   45       http://rumahdijual.com/depok/1138984-rumah-strategis-pitara-kota-depok.html                              
    500     80   45       http://rumahdijual.com/depok/1126663-hunian-dalam-cluster-di-jalan-pitara-raya.html                      
    500     80   45       http://rumahdijual.com/depok/1124365-one-gate-system.html                                                
    500     80   40       http://rumahdijual.com/depok/865066-taman-bumi-agung-residence-aman-nyaman-alami-sawangan-depok.html     
    500     80   40       http://rumahdijual.com/depok/1272094-rumah-nempel-dengan-jakarta-selatan-ditanah-baru-depok.html         
    500     80   40       http://rumahdijual.com/depok/916629-rumah-dijual-hunian-strategis-dan-harga-minimalis.html               
    500     80   40       http://rumahdijual.com/depok/933648-hanya-dengan-dp-20-gun-sudah-bisa-punya-rumah.html                   
    500     78   54       http://rumahdijual.com/depok/916512-rumah-dengan-harga-terjangkau-di-belakang-dtc-depok.html             
    500     78   36       http://rumahdijual.com/depok/1191569-cluster-baru-di-gdc.html                                            
    500     77   42       http://rumahdijual.com/depok/1038937-rumah-uang-muka-ringan-bgt-exit-tol-cimanggis.html                  
    500     76   38       http://rumahdijual.com/depok/1303001-rumah-depok-murah.html                                              
    500     75   50       http://rumahdijual.com/depok/1068350-rumah-idaman.html                                                   
    500     75   10       http://rumahdijual.com/depok/1110137-rumah-murah-beji-pladen-ditengah-kota-depok.html                    
    500     74   42       http://rumahdijual.com/depok/1184746-rumah-kalimulya-depok.html                                          
    500     72   45       http://rumahdijual.com/depok/922585-rumah-secondary-lokasi-tanah-baru-beji-depok-fasilitas-komplit.html  
    500     72   45       http://rumahdijual.com/depok/1302378-jual-rumah-cantik-lokasi-strategis.html                             
    500     72   45       http://rumahdijual.com/depok/1230989-rumah-baru-siap-huni-curug-tanah-baru-matoa-golf.html               
    500     72   45       http://rumahdijual.com/depok/1298612-rumah-dijual-murah-banget-bonus-furniture-disawangan-depok.html     
    500     72   43       http://rumahdijual.com/depok/919095-rumah-strategis-di-depok.html                                        
    500     72   40       http://rumahdijual.com/depok/923534-perumahan-murah-lokasi-strategis-di-pancoran-mas-depok.html          
    500     72   40       http://rumahdijual.com/depok/1234628-rumah-murah-depok.html                                              
    500     72   40       http://rumahdijual.com/depok/1225396-rumah-minimalis-murah-depok.html                                    
    500     72   38       http://rumahdijual.com/depok/1111915-rumah-minimalis-nan-cantik-di-depok.html                            
    500     72   30       http://rumahdijual.com/depok/856844-rumah-di-depok-type-30-72-permata-cimanggis-dp.html                  
    500     72   30       http://rumahdijual.com/depok/1182907-rumah-cluster-di-depok.html                                         
    500     70   36       http://rumahdijual.com/depok/1197062-di-jual-rmh-kmpg-bu-lt-70-m-shm.html                                
    500     65   45       http://rumahdijual.com/depok/1205515-dijual-rumah-cluster-mini.html                                      
    500     65   45       http://rumahdijual.com/depok/1202426-rumah-baru-dalam-cluster-di-tanah-baru-500-juta.html                
    500     45   45       http://rumahdijual.com/depok/970366-rumah-2-lantai-unik-baru-renov-nyaman-lingkungan-nyaman.html
    

## House Price Between 500 - 600 Mio IDR

### VIsualize Data


```python
df = visualizeData('depok', 500, 600);
```


![png](png/output_50_0.png)


### Analyze the Data of House Price Between 500 - 600 Mio IDR


```python
avg = averageMeasures(df)
```

    
    AVERAGE MEASURES
    -----------------
    
    building    64
        land    98
       price   550
    


```python
mostSpacious(df)
```

    
    MOST SPACIOUS LAND
    -----------------
    
        bath     1
         bed     1
    building   135
        land   430
       price   550
         url   http://rumahdijual.com/depok/469169-dijual-rumah-kontrakan-di-jatijajar-cimanggis-depok.html
    
    MOST SPACIOUS BUILDING
    -----------------
    
        bath     2
         bed     4
    building   250
        land   377
       price   500
         url   http://rumahdijual.com/depok/1000412-rumah-murah-di-depok.html
    


```python
selectEconomical(df, avg, unit)
```

    
    MOST ECONOMICAL
    -----------------
    is when the price is really below average: 550 (million IDR) but you get above the average land: 98 (square meters) and above the average building: 64 (square meters)
    
    You are blessed to choose one of these 190  houses:
    
    price  land building                                                                                                        url
    500     377   250      http://rumahdijual.com/depok/1000412-rumah-murah-di-depok.html                                          
    500     309   90       http://rumahdijual.com/depok/891528-rumah-murah-di-tapos-depok.html                                     
    500     309   90       http://rumahdijual.com/depok/855076-dijual-rumah-murah-di-tapos-depok.html                              
    500     200   70       http://rumahdijual.com/depok/1305120-rumah-dijual-kampung-kebon-cinangka-dekat-kubah-emas-sawangan.html 
    500     200   250      http://rumahdijual.com/depok/1307113-di-jual-rumah-jalan-raya-pekapuran-siap-huni.html                  
    500     180   180      http://rumahdijual.com/depok/1058776-jual-cepat-rumah-siap-huni-di-sawangan-depok-bojongsari.html       
    500     160   90       http://rumahdijual.com/depok/971918-kavling-abdul-wahab-mengapa-tunggu-sampai-besok.html                
    500     160   160      http://rumahdijual.com/depok/1088598-rumah-dekat-perapatan-uki-pitara.html                              
    500     150   75       http://rumahdijual.com/depok/1314614-di-jual-rumah-terjangkau-luas-tanah-150m-sawangan-depok.html       
    500     150   120      http://rumahdijual.com/depok/733955-rumah-bekas-daerah-pondok-petir-depok-ada-warungnya.html            
    500     150   100      http://rumahdijual.com/depok/889788-rumah-dijual-cepat-bu.html                                          
    500     140   70       http://rumahdijual.com/depok/1253000-luas-murah-asri-di-mekarsari-cimanggis.html                        
    500     139   70       http://rumahdijual.com/depok/1015868-rumah-siap-huni-3-kamar-di-pitara-depok.html                       
    500     135   120      http://rumahdijual.com/depok/1307861-urun-harga-rumah-di-sukatani-dari-600-jt-turun.html                
    500     129   80       http://rumahdijual.com/depok/937422-cluster-permata-ruby.html                                           
    500     129   70       http://rumahdijual.com/depok/948519-rumah-luas-harga-murah.html                                         
    500     125   75       http://rumahdijual.com/depok/1051903-rumah-akses-tol-dan-lrt-cimanggis-de-residence.html                
    500     122   75       http://rumahdijual.com/depok/876937-dijual-rumah-murah-strategis-perbatasan-depok-dan-jakarta.html      
    500     122   100      http://rumahdijual.com/depok/1142914-rumah-dijual-di-depok.html                                         
    500     111   100      http://rumahdijual.com/depok/689239-rumah-dekat-stasiun-citayam-depok.html                              
    500     110   80       http://rumahdijual.com/depok/1301686-rumah-di-kali-mulya-depok-siap-huni.html                           
    500     110   80       http://rumahdijual.com/depok/1186555-rumah-di-kali-mulya-mandor.html                                    
    500     110   70       http://rumahdijual.com/depok/1050762-rumah-baru-110-mtr-kalimulya-dkt-gdc-depok.html                    
    500     110   100      http://rumahdijual.com/depok/962364-rumah-minimalis-baru-cipayung-depok.html                            
    500     107   70       http://rumahdijual.com/depok/1256573-hunian-minimalis-dekat-pusat-kota.html                             
    500     107   70       http://rumahdijual.com/depok/1256565-rumah-minimalis-dekat-pusat-kota.html                              
    500     107   70       http://rumahdijual.com/depok/1248255-rumah-luas-3-kamar-tidur-dekat-pusat-kota.html                     
    500     107   70       http://rumahdijual.com/depok/1259210-rumah-minimalis-3-kamar-tidur-2-kamar-mandi-dekat.html             
    500     107   70       http://rumahdijual.com/depok/1259209-rumah-manis-dekat-pusat-kota-depok.html                            
    500     105   90       http://rumahdijual.com/depok/740291-di-jual-rumah-cantik-siap-huni-di-permata-depok.html                
    500     105   70       http://rumahdijual.com/depok/1112380-rumah-ready-stock-di-jalan-raya-pitara-depok.html                  
    500     105   65       http://rumahdijual.com/depok/1038494-rumah-besar-3-kamar-harga-2-kamar-dekat-stasiun.html               
    500     105   65       http://rumahdijual.com/depok/1108420-rumah-besar-3-kamar-harga-2-kamar-dekat-stasiun.html               
    500     104   70       http://rumahdijual.com/depok/1310477-rumah-minimalis-dekat-pusat-kota-depok.html                        
    500     104   70       http://rumahdijual.com/depok/1310495-stop-beli-rumah-foto-palsu-harga-murah.html                        
    500     104   70       http://rumahdijual.com/depok/1310507-stop-beli-rumah-dengan-foto-iklan-palsu-dan-harga.html             
    500     104   70       http://rumahdijual.com/depok/1313392-permata-regency-kota-depok.html                                    
    500     104   70       http://rumahdijual.com/depok/1305223-rumah-minimalis-bisa-dicicil-pribadi-ke-owner-langsung.html        
    500     104   70       http://rumahdijual.com/depok/1310542-stop-beli-rumah-dengan-foto-iklan-palsu.html                       
    500     104   65       http://rumahdijual.com/depok/1313402-rumah-cantik-dekat-pusat-kota.html                                 
    500     104   65       http://rumahdijual.com/depok/1040296-rumah-lokasi-strategis-aman-dan-nyaman.html                        
    500     104   65       http://rumahdijual.com/depok/1036730-investasi-cerdas-untuk-masa-depan.html                             
    500     104   65       http://rumahdijual.com/depok/1118356-rumah-baru-harga-murah-tahun-sekarang-tahun-depan-mahal.html       
    500     102   90       http://rumahdijual.com/depok/996103-dijual-rumah-di-depok-lokasi-strategis-5menit-dari-margonda.html    
    500     100   90       http://rumahdijual.com/depok/978724-rumah-dekat-jalan-raya-citayam-depok.html                           
    500     100   90       http://rumahdijual.com/depok/1231173-dijual-rumah-baru.html                                             
    500     100   80       http://rumahdijual.com/depok/1056112-rumah-cluster-di-pitara-kota-depok-strategis.html                  
    500     100   80       http://rumahdijual.com/depok/1078966-rumah-cluster-strategis-siapa-yang-suka.html                       
    500     100   80       http://rumahdijual.com/depok/1089183-hunian-nyaman-dan-asri-one-gate-system.html                        
    500     100   80       http://rumahdijual.com/depok/1068230-rumah-cluster-pitara-kota-depok.html                               
    500     100   80       http://rumahdijual.com/depok/1078548-rumah-cluster-one-gate-system-pitara-pancoran-mas-depok.html       
    500     100   80       http://rumahdijual.com/depok/1078466-rumah-cluster-one-gate-system-pitara-pancoran-mas-depok.html       
    500     100   80       http://rumahdijual.com/depok/1083970-hunian-cluster-pitara-pancoran-mas-depok-one-gate-system.html      
    500     100   80       http://rumahdijual.com/depok/1083983-one-gate-system-cluster-pitara-pancoran-mas-kota-depok.html        
    500     100   80       http://rumahdijual.com/depok/1301724-rumah-di-depok-kali-mulya.html                                     
    500     100   80       http://rumahdijual.com/depok/1072831-cluster-100m2-pitara-depok.html                                    
    500     100   80       http://rumahdijual.com/depok/1045264-rumah-cluster-di-pitara-kota-depok.html                            
    500     100   80       http://rumahdijual.com/depok/1077652-rumah-cluster-pitara-pancoran-mas-depok.html                       
    500     100   80       http://rumahdijual.com/depok/1056815-cluster-murah-banyak-pilihan.html                                  
    500     100   80       http://rumahdijual.com/depok/1070868-rumah-cluster-pitara-pancoran-mas-kota-depok.html                  
    500     100   80       http://rumahdijual.com/depok/1065338-rumah-cluster-depok-pitara.html                                    
    500     100   80       http://rumahdijual.com/depok/1115852-rumah-type-80-100-m-di-jln-pitara-pancoran.html                    
    500     100   80       http://rumahdijual.com/depok/1056044-rumah-cluster-pitara-kota-depok.html                               
    500     100   80       http://rumahdijual.com/depok/1078412-rumah-cluster-one-gate-system-pitara-pancoran-mas-depok.html       
    500     100   80       http://rumahdijual.com/depok/1064106-rumah-cluster-pitara-kota-depok.html                               
    500     100   80       http://rumahdijual.com/depok/1134295-rumah-tingkat-harga-gak-bikin-melarat.html                         
    500     100   80       http://rumahdijual.com/depok/1064272-cluster-depok-30meter-ke-jalur-angkot.html                         
    500     100   80       http://rumahdijual.com/depok/1072600-cluster-pitara-depok-nyaman-dan-bebas-banjir.html                  
    500     100   80       http://rumahdijual.com/depok/1058835-rumah-type-80-100-lokasi-strategis-depok.html                      
    500     100   80       http://rumahdijual.com/depok/1097213-properti-grya-pratama-asri-kota-depok.html                         
    500     100   80       http://rumahdijual.com/depok/1067256-rumah-di-depok-pitara.html                                         
    500     100   80       http://rumahdijual.com/depok/1055126-rumah-cluster-di-pitara-depok.html                                 
    500     100   80       http://rumahdijual.com/depok/1112478-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html       
    500     100   80       http://rumahdijual.com/depok/1050675-rumah-cluster-pitara-depok.html                                    
    500     100   80       http://rumahdijual.com/depok/1042875-rumah-cluster-pitara-depok.html                                    
    500     100   80       http://rumahdijual.com/depok/1042700-rumah-cluster-pitara-depok-lantai-full-granit.html                 
    500     100   80       http://rumahdijual.com/depok/1178394-rumah-ready-stock-tanah-100-a.html                                 
    500     100   80       http://rumahdijual.com/depok/1221054-rumah-dekat-pusat-kota-depok.html                                  
    500     100   80       http://rumahdijual.com/depok/1092348-rumah-cluster-pitara-pancoran-mas-depok.html                       
    500     100   80       http://rumahdijual.com/depok/1060871-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html        
    500     100   80       http://rumahdijual.com/depok/1068182-rumah-cluster-pitara-kota-depok.html                               
    500     100   80       http://rumahdijual.com/depok/1060869-rumah-cluster-pitara-kota-depok.html                               
    500     100   80       http://rumahdijual.com/depok/1055491-rumah-cluster-di-pitara-kota-depok-strategis.html                  
    500     100   80       http://rumahdijual.com/depok/1094200-rumah-cluster-kemana-mana-deket.html                               
    500     100   80       http://rumahdijual.com/depok/1094205-rumah-cluster-pancoran-mas-depok.html                              
    500     100   80       http://rumahdijual.com/depok/1056086-rumah-cluster-pitara-kota-depok.html                               
    500     100   80       http://rumahdijual.com/depok/1044218-rumah-cluster-minimalis-di-pitara-depok.html                       
    500     100   80       http://rumahdijual.com/depok/1221211-rumah-cluster-one-gate-system.html                                 
    500     100   80       http://rumahdijual.com/depok/1226248-mandala-golden-residence-sawangan-kota-depok-promo-discount-dp.html
    500     100   70       http://rumahdijual.com/depok/1112152-hunian-cluster-one-gate-system-di-jalan-pitara.html                
    500     100   70       http://rumahdijual.com/depok/1112341-rumah-cluster-jalan-pitara-raya-kota-depok.html                    
    500     100   70       http://rumahdijual.com/depok/1112460-rumah-cluster-pitara-pancoran-mas-kota-depok.html                  
    500     100   70       http://rumahdijual.com/depok/1112454-rumah-cluster-one-gate-system-pitara-pancoran-mas-depok.html       
    500     100   70       http://rumahdijual.com/depok/1112122-hunian-cluster-di-pitara-pancoran-mas-kota-depok.html              
    500     100   70       http://rumahdijual.com/depok/1110603-rumah-cluster-pitara-kota-depok.html                               
    500     100   70       http://rumahdijual.com/depok/1102323-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html        
    500     100   70       http://rumahdijual.com/depok/1104426-hunian-cluster-depok.html                                          
    500     100   70       http://rumahdijual.com/depok/1103839-rumah-cluster-one-gate-system.html                                 
    500     100   70       http://rumahdijual.com/depok/1244205-hunian-cluster-di-pitara-kota-depok-lantai-full-granit.html        
    500     100   70       http://rumahdijual.com/depok/1244195-griya-pratama-asri-siap-huni.html                                  
    500     100   70       http://rumahdijual.com/depok/1207444-cluster-banyak-pilihan-depok.html                                  
    500     100   70       http://rumahdijual.com/depok/1209407-rumah-cluster-di-pitara-kota-depok-strategis.html                  
    500     100   70       http://rumahdijual.com/depok/1208901-rumah-luas-harga-luas-depok.html                                   
    500     100   70       http://rumahdijual.com/depok/1207442-cluster-banyak-pilihan-depok.html                                  
    500     100   70       http://rumahdijual.com/depok/1058839-rumah-15-menit-ke-pusat-kota-depok.html                            
    500     100   70       http://rumahdijual.com/depok/1229279-hunian-cluster-di-pitara-kota-depok-lantai-full-granite.html       
    500     100   70       http://rumahdijual.com/depok/1209087-iklan-foto-asli.html                                               
    500     100   70       http://rumahdijual.com/depok/1222593-griya-pratama-asri-siap-huni.html                                  
    500     100   70       http://rumahdijual.com/depok/1233760-hunian-cluster-di-pitara-kota-depok-lantai-full-granit.html        
    500     100   70       http://rumahdijual.com/depok/1229175-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html        
    500     100   70       http://rumahdijual.com/depok/1207191-rumah-dalam-cluster-one-gate-system.html                           
    500     100   70       http://rumahdijual.com/depok/1209195-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html       
    500     100   70       http://rumahdijual.com/depok/1110579-rumah-cluster-pitara-kota-depok.html                               
    500     100   70       http://rumahdijual.com/depok/1112449-hunian-cluster-one-gate-system.html                                
    500     100   70       http://rumahdijual.com/depok/1150849-hunian-luas-harga-murah-depok.html                                 
    500     100   70       http://rumahdijual.com/depok/1298549-rumah-cluster-pitara-pancoran-mas-kota-depok.html                  
    500     100   70       http://rumahdijual.com/depok/1270942-rumah-siap-huni-dan-bersertifikat-di-pitara-depok.html             
    500     100   70       http://rumahdijual.com/depok/1243169-griya-pratama-asri-siap-huni.html                                  
    500     100   70       http://rumahdijual.com/depok/1229258-rumah-cluster-pitara-kota-depok.html                               
    500     100   70       http://rumahdijual.com/depok/1293541-rumah-strategis-keamanan-24jam-di-pitara-depok.html                
    500     100   70       http://rumahdijual.com/depok/1238260-rumah-cluster-pitara.html                                          
    500     100   70       http://rumahdijual.com/depok/1128317-rumah-baru-harga-seru-pitara-kota-depok.html                       
    500     100   70       http://rumahdijual.com/depok/1150833-rumah-cluster-di-pitara-depok.html                                 
    500     100   70       http://rumahdijual.com/depok/1191949-rumah-cluster-one-gate-system.html                                 
    500     100   70       http://rumahdijual.com/depok/1191951-rumah-luas-harga-murah-di-pitara-depok.html                        
    500     100   70       http://rumahdijual.com/depok/1137981-rumah-manis-gaya-minimalis-kota-depok.html                         
    500     100   70       http://rumahdijual.com/depok/1137985-rumah-cluster-banyak-tipe-depok.html                               
    500     100   70       http://rumahdijual.com/depok/1150832-hunian-strategis-cocok-unt-invest.html                             
    500     100   70       http://rumahdijual.com/depok/1137997-hunian-asri-minimalis-depok.html                                   
    500     100   70       http://rumahdijual.com/depok/1145555-hunian-strategis-kemana-mana-dekat.html                            
    500     100   70       http://rumahdijual.com/depok/1145611-rumah-manis-minimalis-dan-strategis-depok.html                     
    500     100   70       http://rumahdijual.com/depok/1112468-rumah-cluster-jalan-pitara-pancoran-mas-depok.html                 
    500     100   70       http://rumahdijual.com/depok/1110858-hunian-cluster-di-pitara-pancoran-mas-kota-depok.html              
    500     100   70       http://rumahdijual.com/depok/1063752-rumah-cluster-di-pitara-kota-depok-strategis.html                  
    500     100   70       http://rumahdijual.com/depok/1177139-rumah-baru-ready-dan-indet-pitara-depok.html                       
    500     100   70       http://rumahdijual.com/depok/1175000-hunian-di-lokasi-strategis-pitara-depok.html                       
    500     100   70       http://rumahdijual.com/depok/1175009-rumah-adem-harga-tentrem.html                                      
    500     100   70       http://rumahdijual.com/depok/1112496-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html       
    500     100   70       http://rumahdijual.com/depok/1145594-hunian-harga-murah-pitara-depok.html                               
    500     100   70       http://rumahdijual.com/depok/1112602-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html       
    500     100   70       http://rumahdijual.com/depok/1078510-rumah-dekat-jalan-villa-santika.html                               
    500     100   70       http://rumahdijual.com/depok/1110523-rumah-cluster-pitara-kota-depok.html                               
    500     100   70       http://rumahdijual.com/depok/1056761-rumah-cluster-pitara-kota-depok.html                               
    500     100   70       http://rumahdijual.com/depok/1112617-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html       
    500     100   70       http://rumahdijual.com/depok/1232231-rumah-kota-depok.html                                              
    500     100   70       http://rumahdijual.com/depok/1182896-rumah-cluster-one-gate-system-ready-stock.html                     
    500     100   65       http://rumahdijual.com/depok/1242539-rumah-minimalis-nempel-perumahan-permata-regency-kota-depok.html   
    500     100   65       http://rumahdijual.com/depok/1209422-rumah-cluster-di-lokasi-strategis-depok.html                       
    500     100   65       http://rumahdijual.com/depok/1209389-rumah-cluster-pitara-kota-depok.html                               
    500     100   65       http://rumahdijual.com/depok/1239879-cluster-elit-harga-irit.html                                       
    500     100   65       http://rumahdijual.com/depok/1095142-rumah-cluster-kemna-mana-dekat.html                                
    500     100   65       http://rumahdijual.com/depok/1242590-rumah-minimalis-dekat-pusat-kota.html                              
    500     100   65       http://rumahdijual.com/depok/1242584-rumah-minimalis-nempel-perumahan-permata-regency-kota-depok.html   
    500     100   65       http://rumahdijual.com/depok/1100084-rumah-cluster-pancoran-mas-depok.html                              
    500     100   65       http://rumahdijual.com/depok/1099761-cluster-pitara-kec-pancoran-mas-depok.html                         
    500     100   65       http://rumahdijual.com/depok/1099796-rumah-cluster-di-lokasi-strategis-pitara-kota-depok.html           
    500     100   65       http://rumahdijual.com/depok/980977-rumah-mini-cluster-cipayung-depok.html                              
    500     100   65       http://rumahdijual.com/depok/1228396-rumah-cluster-nempel-permata-regency.html                          
    500     100   65       http://rumahdijual.com/depok/1094197-rumah-cluster-pitara-depok.html                                    
    500     100   65       http://rumahdijual.com/depok/1094207-rumah-cluster-ga-cuma-1-type.html                                  
    500     100   160      http://rumahdijual.com/depok/1000271-rumah-2-lantai-di-harjamukti-cimanggis-depok.html                  
    500     100   140      http://rumahdijual.com/depok/1114888-rumah-murah-depok.html                                             
    500     100   100      http://rumahdijual.com/depok/1033544-rumah-dua-lantai-komplek-gobel-mekarsari-depok-bisa-kpr.html       
    520     194   150      http://rumahdijual.com/depok/1172307-di-jual-rumah-dan-toko-tanah-luas-di-rawa.html                     
    520     180   110      http://rumahdijual.com/depok/1273387-di-jual-rumah-tanah-luas-harga-cantik-di-kalimulya.html            
    520     105   85       http://rumahdijual.com/depok/1124793-rumah-bagus-satu-setengah-lantai-siap-huni-di-meruyung.html        
    520     100   80       http://rumahdijual.com/depok/1065259-rumah-cluster-pitara-kota-depok.html                               
    525     405   170      http://rumahdijual.com/depok/1206149-rumah-strategis-di-daerah-yang-sedang-berkembang-di-sasak.html     
    525     260   200      http://rumahdijual.com/depok/836710-rumah-lt-260-lb-200-lokasi-strategis-depan-pesantren.html           
    525     130   100      http://rumahdijual.com/depok/507867-jual-rumah-shm-di-jl-pendidikan-cinangka-sawangan-depok.html        
    525     126   100      http://rumahdijual.com/depok/1121701-rumah-usaha-tipe-100-126-rp-525jt-nego-jl.html                     
    525     121   85       http://rumahdijual.com/depok/944587-rumah-baru-harga-murah-jual-cepat.html                              
    525     120   80       http://rumahdijual.com/depok/1249959-dijual-rumah-scond-di-villa-pertiwi-depok-jawa-barat.html          
    525     120   80       http://rumahdijual.com/depok/1071215-rumah-paling-murah-di-depok.html                                   
    525     120   80       http://rumahdijual.com/depok/1069574-dijual-rumah-1-lantai-di-jalan-raya-bogor-villa.html               
    525     120   66       http://rumahdijual.com/depok/808918-stop-beli-rumah-yang-asal-bangun-beli-rumah-disini.html             
    525     120   65       http://rumahdijual.com/depok/967816-cari-rumah-baca-dulu-nih-tips-nya.html                              
    525     120   100      http://rumahdijual.com/depok/939055-dijual-rumah-hook-murah.html                                        
    525     100   70       http://rumahdijual.com/depok/1180500-rumah-kota-depok-baru-strategis.html                               
    530     281   70       http://rumahdijual.com/depok/1185748-rumah-masuk-1-mobil-di-raden-saleh-depok-r21.html                  
    530     110   90       http://rumahdijual.com/depok/913202-dijual-rumah-siap-huni-bagus-dan-murah-bisa-kpr.html                
    530     110   90       http://rumahdijual.com/depok/898126-dijual-cepat-rumah-minimalis-strategis.html                         
    530     105   65       http://rumahdijual.com/depok/1133895-rumah-murah-di-pitara-depok.html                                   
    530     105   65       http://rumahdijual.com/depok/1128709-rumah-murah-harga-gak-bikin-gerah.html                             
    530     105   65       http://rumahdijual.com/depok/1128688-rumah-besar-harga-nyasar.html                                      
    530     100   70       http://rumahdijual.com/depok/1148127-rumah-cluster-depok-pitara-raya.html                               
    540     130   100      http://rumahdijual.com/depok/909013-rumah-cantik-kalimulya-depok.html                                   
    540     126   73       http://rumahdijual.com/depok/909005-rumah-cantik-kalimulya-depok.html                                   
    540     119   75       http://rumahdijual.com/depok/646819-rumah-di-jl-cemara-grogol-depok.html                                
    545     115   80       http://rumahdijual.com/depok/1298819-17-di-jual-rumah-baru-siap-huni-kalimulya-depok.html
    


```python
selectModerate(df, avg, unit)
```

    
    MODERATE PRICE
    -----------------
    is when the price is above average: 550 (million IDR) with above-average land: 98 (square meters) and above-average building: 64 (square meters)
    
    
    There are : 393  items with above-average price and above-average land.
    
    There are : 254  items with above-average price, above-average land and above-average building.
    
    price  land building                                                                                                              url
    550     98    90       http://rumahdijual.com/depok/1224057-rumah-baru-5m-jalur-angkot.html                                          
    550     98    90       http://rumahdijual.com/depok/899971-rumah-baru-bagus-jalur-angkot.html                                        
    550     98    90       http://rumahdijual.com/depok/974358-jual-rumah-siap-huni-shm-di-cinangka-depok-tanpa.html                     
    550     98    90       http://rumahdijual.com/depok/869068-rumah-di-bbm-jln-h-dimun.html                                             
    550     430   135      http://rumahdijual.com/depok/469169-dijual-rumah-kontrakan-di-jatijajar-cimanggis-depok.html                  
    550     248   89       http://rumahdijual.com/depok/1084394-hunian-bagus-harga-bersahabat-daerah-tapos.html                          
    550     225   160      http://rumahdijual.com/depok/1290543-rumah-di-jatijajar-depok.html                                            
    550     200   185      http://rumahdijual.com/depok/274144-di-jual-rumah-dan-kontrakan-dekat-jalan-raya-citayam.html                 
    550     200   110      http://rumahdijual.com/depok/1240962-rumah-strategis-dicimanggis-depok.html                                   
    550     200   110      http://rumahdijual.com/depok/1145451-rumah-murah-dijual-di-sukatani-cimanggis-depok-jual-butuh.html           
    550     200   110      http://rumahdijual.com/depok/1149649-rumah-strategis.html                                                     
    550     187   165      http://rumahdijual.com/depok/1255276-lt-187-m2-ajb-sawangan-bedahan-550-juta.html                             
    550     185   160      http://rumahdijual.com/depok/1277120-dijual-rumah-di-daerah-depok-jawa-barat-jabodetabek.html                 
    550     173   150      http://rumahdijual.com/depok/914177-jual-rumah-plus-kontrakan-2-pintu.html                                    
    550     151   100      http://rumahdijual.com/depok/945519-vila-pamulang-jl-rajawali-3-a.html                                        
    550     147   100      http://rumahdijual.com/depok/1240194-cluster-minimalis-pamulang-dp-seadanya.html                              
    550     147   100      http://rumahdijual.com/depok/1241305-cluster-dream-sisa-1-unit-dp-seadanya-bojongsari-depok.html              
    550     147   100      http://rumahdijual.com/depok/1241306-rumah-cluster-second-bisa-kpr-di-pondok-petir-bojongsari.html            
    550     140   130      http://rumahdijual.com/depok/1200134-dijual-rumah-baru-strategis-di-tanah-baru-depok-pr808.html               
    550     135   125      http://rumahdijual.com/depok/1175562-rumah-dijual-di-daerah-sukatani-bebas-banjir-aman-dan.html               
    550     135   120      http://rumahdijual.com/depok/1183256-dijual-rumah-di-sukatani-depok.html                                      
    550     135   120      http://rumahdijual.com/depok/1303436-jual-cepat-rumah-murah-di-perumahan-sukatani.html                        
    550     135   120      http://rumahdijual.com/depok/1306682-dijual-rumah-di-sukatani-permai-depok.html                               
    550     135   100      http://rumahdijual.com/depok/894910-rumah-diijual-di-depok-pancoran-mas.html                                  
    550     135   100      http://rumahdijual.com/depok/910511-rumah-di-jual-di-depok-lama-dekat-stasiun.html                            
    550     123   100      http://rumahdijual.com/depok/984998-rumah-di-jual-di-depok.html                                               
    550     120   80       http://rumahdijual.com/depok/938658-rumah-strategis-di-depok-dua-r21-0280-a.html                              
    550     120   131      http://rumahdijual.com/depok/1243887-rumah-poin-mas-depok.html                                                
    550     120   110      http://rumahdijual.com/depok/615098-rumah-bnew-ada-3-unit-di-depok.html                                       
    550     117   85       http://rumahdijual.com/depok/943586-rumah-dijual-lokasi-serua-raya-pondok-petir.html                          
    550     117   76       http://rumahdijual.com/depok/893340-rumah-yang-sangat-dekat-dengan-pusat-kota-dan-cocok.html                  
    550     114   66       http://rumahdijual.com/depok/780016-rumah-type-66-114-meruyung-depok.html                                     
    550     112   75       http://rumahdijual.com/depok/1240408-rumah-dijual-cepat.html                                                  
    550     112   120      http://rumahdijual.com/depok/1192064-jual-murah-perumahan-poin-mas-depok.html                                 
    550     111   70       http://rumahdijual.com/depok/935792-rumah-minimalis-cantik-di-pancoran-mas-depok.html                         
    550     110   70       http://rumahdijual.com/depok/1014034-rumah-one-gate-system-kota-depok.html                                    
    550     110   65       http://rumahdijual.com/depok/1073663-rumah-murah-dekat-stasiun-di-kavling-kencana.html                        
    550     105   80       http://rumahdijual.com/depok/909406-rumah-second-3-kamar-tidur-lokasi-nempel-ciganjur-jakarta.html            
    550     105   65       http://rumahdijual.com/depok/1125389-rumah-adem-semeriwing-harga-miring.html                                  
    550     105   65       http://rumahdijual.com/depok/1089957-rumah-kokoh-harga-jatoh.html                                             
    550     102   80       http://rumahdijual.com/depok/1031797-perumnas-depok-2-tengah-100-meter-jalur-angkot-15-a.html                 
    550     101   75       http://rumahdijual.com/depok/992010-kemang-swatama-hunian-asri-di-daerah-cilodong.html                        
    550     100   90       http://rumahdijual.com/depok/1120328-rumah-5-meter-jalutr-angkot.html                                         
    550     100   80       http://rumahdijual.com/depok/1221088-rumah-luas-lega-buat-keluarga-anda.html                                  
    550     100   80       http://rumahdijual.com/depok/1229514-rumah-nyaman-pitara-depok.html                                           
    550     100   80       http://rumahdijual.com/depok/1181561-rumah-baru-cluster.html                                                  
    550     100   70       http://rumahdijual.com/depok/1050741-rumah-di-pitara-depok-rumah-besar-untuk-keluarga-besar.html              
    550     100   70       http://rumahdijual.com/depok/880894-rumah-cluster-dengan-lt-100m.html                                         
    550     100   70       http://rumahdijual.com/depok/1177803-properti-kota-depok-pitara.html                                          
    550     100   70       http://rumahdijual.com/depok/1181509-rumah-baru-siap-huni-jln-pitara.html                                     
    550     100   70       http://rumahdijual.com/depok/1185459-rumah-cluster-pitara-kota-depok.html                                     
    550     100   70       http://rumahdijual.com/depok/1177328-rumah-cluster-kota-depok-pancoran-mas.html                               
    550     100   70       http://rumahdijual.com/depok/1171181-rumah-strategis-pitara-kota-depok.html                                   
    550     100   70       http://rumahdijual.com/depok/1189128-rumah-cluster-kota-depok.html                                            
    550     100   70       http://rumahdijual.com/depok/1176698-rumah-mewah-harga-murah.html                                             
    550     100   70       http://rumahdijual.com/depok/1224284-miliki-rumahnya-dapatkan-kemewahannya-kavling-jatimulya.html             
    550     100   65       http://rumahdijual.com/depok/1082302-rumah-asri-dan-cantik-di-cilodong-depok.html                             
    550     100   64       http://rumahdijual.com/depok/1060624-cluster-depok.html                                                       
    551     98    75       http://rumahdijual.com/depok/694196-town-house-pabuaran-village-rumah-cantik-harga-menarik.html               
    551     105   75       http://rumahdijual.com/depok/1069684-rumah-di-bukit-rivaria-sawangan-depok.html                               
    555     99    75       http://rumahdijual.com/depok/693614-town-house-pabuaran-village-rumah-cantik-harga-menarik.html               
    555     105   90       http://rumahdijual.com/depok/938472-rumah-5-menit-ke-ui-depok.html                                            
    560     105   75       http://rumahdijual.com/depok/1064266-rumah-lelang-di-bukit-rivaria-sawangan-depok.html                        
    560     102   90       http://rumahdijual.com/depok/1120221-rumah-megah-harga-rendah-perumnas-depok-timur.html                       
    565     240   120      http://rumahdijual.com/depok/926186-rumah-luas-di-lokasi-yang-asri.html                                       
    565     150   100      http://rumahdijual.com/depok/1105926-stop-beli-rumah-yang-asal-bangun-beli-rumah-di.html                      
    565     150   100      http://rumahdijual.com/depok/1291696-rumah-cluster-modern-harga-murah-di-citayam-susukan.html                 
    565     150   100      http://rumahdijual.com/depok/1291788-ayo-buruan-beli-sekarang-semakin-di-tunda2-makin-mahal.html              
    565     150   100      http://rumahdijual.com/depok/1291695-rumah-minimalist-murah-dan-lingkungan-yang-sehat.html                    
    565     150   100      http://rumahdijual.com/depok/1291773-cluster-modern-harga-murah-meriah.html                                   
    565     150   100      http://rumahdijual.com/depok/1065787-rumah-sederhana-berkualitas-di-susukan-citayam.html                      
    565     150   100      http://rumahdijual.com/depok/1292825-rumah-idaman-dan-modern-termurah.html                                    
    565     150   100      http://rumahdijual.com/depok/1292824-rumah-cluster-one-gate-system.html                                       
    565     150   100      http://rumahdijual.com/depok/1291693-cluster-murah-unit-terbatas-lokasi-strategis.html                        
    565     150   100      http://rumahdijual.com/depok/1291387-cluster-modern-harga-murah-meriah.html                                   
    565     150   100      http://rumahdijual.com/depok/1291352-rumah-impian-pabuaran-susukan-citayam.html                               
    565     150   100      http://rumahdijual.com/depok/1297191-cari-rumah-murah-dan-nyaman-disini-tempat-nya.html                       
    565     150   100      http://rumahdijual.com/depok/1291784-cluster-tercantik-di-citayam-dekat-dengan-stasiun.html                   
    565     150   100      http://rumahdijual.com/depok/1311804-cluster-mutiara-dengan-bnyak-pasilitas-menunjang.html                    
    565     150   100      http://rumahdijual.com/depok/1298349-rumah-nyaman-terlaris-di-depok.html                                      
    565     150   100      http://rumahdijual.com/depok/1312214-cluster-mutiara-dengan-bnyak-pasilitas-menunjang.html                    
    565     150   100      http://rumahdijual.com/depok/1290221-hunian-asri-dekat-stasiun-citayam.html                                   
    565     150   100      http://rumahdijual.com/depok/1315713-hunian-terbaru-dikelilingi-perumahan.html                                
    565     150   100      http://rumahdijual.com/depok/1292748-rumah-oke-harga-gak-bikin-boke.html                                      
    565     150   100      http://rumahdijual.com/depok/1291485-ayo-buruan-beli-sekarang-semakin-di-tunda2-makin-mahal.html              
    565     150   100      http://rumahdijual.com/depok/1291486-rumah-impian-pabuaran-susukan-citayam.html                               
    565     150   100      http://rumahdijual.com/depok/1292994-rumah-idaman-dan-modern-termurah.html                                    
    565     150   100      http://rumahdijual.com/depok/1298140-rumah-siap-huni-shm-bebas-banjir.html                                    
    565     150   100      http://rumahdijual.com/depok/1311966-cluster-mutiara-dengan-bnyak-pasilitas-menunjang.html                    
    565     150   100      http://rumahdijual.com/depok/1291436-rumah-minimalist-murah-dan-lingkungan-yang-sehat.html                    
    565     150   100      http://rumahdijual.com/depok/1291398-rumah-cluster-modern-harga-murah-di-citayam-susukan.html                 
    565     150   100      http://rumahdijual.com/depok/1096973-rumah-murah-menawan-di-citayam.html                                      
    565     150   100      http://rumahdijual.com/depok/1298730-hunian-aman-nyaman-dan-asri-pabuaran.html                                
    565     150   100      http://rumahdijual.com/depok/1298684-rumah-cluster-minimalis-dengan-segala-kemudahan.html                     
    565     150   100      http://rumahdijual.com/depok/1297190-sekali-lihat-pasti-cocok.html                                            
    565     150   100      http://rumahdijual.com/depok/1289433-rumah-terlaris-di-pabuaran-susukan-citayam-untuk-kebahagian-keluarga.html
    565     150   100      http://rumahdijual.com/depok/1304470-cluster-mutiara-dengan-bnyak-pasilitas-menunjang.html                    
    565     150   100      http://rumahdijual.com/depok/1304703-cluster-mutiara-dengan-bnyak-pasilitas-menunjang.html                    
    565     150   100      http://rumahdijual.com/depok/1312126-hunian-mewah-dan-terlaris-letak-strategis.html                           
    565     150   100      http://rumahdijual.com/depok/1292904-stop-beli-rumah-yang-asal-bangun-beli-rumah-disini.html                  
    565     150   100      http://rumahdijual.com/depok/1292905-rumah-oke-harga-gak-bikin-boke.html                                      
    565     150   100      http://rumahdijual.com/depok/1292906-rumah-murah-5-menit-ke-stasiun-citayam.html                              
    565     150   100      http://rumahdijual.com/depok/1291625-cluster-tercantik-di-citayam-dekat-dengan-stasiun.html                   
    565     150   100      http://rumahdijual.com/depok/1291162-hunian-terbaru-nempel-pesona-citayam.html                                
    565     150   100      http://rumahdijual.com/depok/1291351-rumah-terlaris-di-pabuaran-susukan-citayam-untuk-kebahagian-keluarga.html
    565     150   100      http://rumahdijual.com/depok/1291662-cluster-modern-harga-murah-meriah.html                                   
    565     150   100      http://rumahdijual.com/depok/1291661-rumah-cluster-modern-harga-murah-di-citayam-susukan.html                 
    565     150   100      http://rumahdijual.com/depok/1291659-cluster-murah-unit-terbatas-lokasi-strategis.html                        
    565     150   100      http://rumahdijual.com/depok/1292684-rumah-oke-harga-gak-bikin-boke.html                                      
    565     150   100      http://rumahdijual.com/depok/1292674-beli-rumah-hati-hati-jangan-tergiur-dengan-harga-murah.html              
    565     150   100      http://rumahdijual.com/depok/1291623-rumah-cluster-modern-harga-murah-di-citayam-susukan.html                 
    565     150   100      http://rumahdijual.com/depok/1292685-rumah-cluster-one-gate-system.html                                       
    565     150   100      http://rumahdijual.com/depok/1292746-rumah-anti-galau-harga-terjangkau.html                                   
    565     150   100      http://rumahdijual.com/depok/1292788-stop-beli-rumah-yang-asal-bangun-beli-rumah-disini.html                  
    565     150   100      http://rumahdijual.com/depok/1292790-rumah-idaman-dan-modern-termurah.html                                    
    565     150   100      http://rumahdijual.com/depok/1065889-rumah-citayam-bebas-banjir.html                                          
    565     150   100      http://rumahdijual.com/depok/1292869-rumah-anti-galau-harga-terjangkau.html                                   
    565     150   100      http://rumahdijual.com/depok/1292870-cari-rumah-baca-dulu-nih-tips-nya.html                                   
    565     150   100      http://rumahdijual.com/depok/1292871-rumah-idaman-dan-modern-termurah.html                                    
    565     150   100      http://rumahdijual.com/depok/1289518-sekali-lihat-pasti-cocok.html                                            
    565     150   100      http://rumahdijual.com/depok/1292745-cari-rumah-baca-dulu-nih-tips-nya.html                                   
    565     150   100      http://rumahdijual.com/depok/1291621-rumah-minimalist-murah-dan-lingkungan-yang-sehat.html                    
    565     150   100      http://rumahdijual.com/depok/1291620-cluster-murah-unit-terbatas-lokasi-strategis.html                        
    565     150   100      http://rumahdijual.com/depok/1298297-hunian-nyaman-terbaru-dan-ter-laris-dengan-akses-mudah.html              
    565     150   100      http://rumahdijual.com/depok/1291023-rumah-siap-huni-shm-_.html                                               
    565     150   100      http://rumahdijual.com/depok/444046-rumah-idaman-keluarga-dekat-stasiun-citayam-dan-bojong-gede.html          
    565     150   100      http://rumahdijual.com/depok/448543-rumah-idaman-tahap-6-di-citayam-harga.html                                
    565     147   70       http://rumahdijual.com/depok/1306457-rumah-murah-di-sawangan-depok.html                                       
    565     120   115      http://rumahdijual.com/depok/1142313-rumah-murah-di-limo-depok.html                                           
    565     112   68       http://rumahdijual.com/depok/1118486-rumah-megah-harga-murah-bro.html                                         
    565     100   65       http://rumahdijual.com/depok/982556-rumah-minimalis-ready-stock.html                                          
    570     196   170      http://rumahdijual.com/depok/985006-rumah-di-jual-di-depok.html                                               
    570     119   75       http://rumahdijual.com/depok/1137146-dijual-rumah-119m2-grogol-limo-depok.html                                
    575     275   70       http://rumahdijual.com/depok/1078352-kontrakan-5-pintu-di-jatijajar-depok-cocok-buat-anda.html                
    575     270   165      http://rumahdijual.com/depok/929283-saat-nya-beli-rumah-harga-bejo-rupiah-sudah-keok.html                     
    575     140   100      http://rumahdijual.com/depok/899212-rumah-baru-murah-di-tanah-baru-angkot-ke-stasiun.html                     
    575     126   70       http://rumahdijual.com/depok/1248733-rumah-komplek-depok-lt-126-m-dekat-ke-stasiun.html                       
    575     126   70       http://rumahdijual.com/depok/1244827-town-house-depok-dekat-menuju-stasiun-ka.html                            
    575     126   70       http://rumahdijual.com/depok/1241979-rumah-cluster-depok-5-menit-ke-stasiun-ka.html                           
    575     120   70       http://rumahdijual.com/depok/1309218-rumah-dijual-daerah-tapos-depok-shm-imb-lt-120-a.html                    
    575     120   70       http://rumahdijual.com/depok/1096414-tanah-dipitara-depok-siap-bangun-rumah-shm-120-m2.html                   
    575     120   100      http://rumahdijual.com/depok/912888-rumah-cantik-nyaman-murah-2-kmr-1-kmr-pembantu.html                       
    575     105   80       http://rumahdijual.com/depok/1007343-rumah-cantik-105-meter-di-kompleks-kpr-depok-lama.html                   
    575     102   100      http://rumahdijual.com/depok/1015876-rumah-type-100-102-lokasi-strategis-di-pinggir-jalan.html                
    575     100   90       http://rumahdijual.com/depok/959180-di-jual-rumah-cantik-perumnas-di-depok-1-291-a.html                       
    577     270   165      http://rumahdijual.com/depok/945022-dollar-mencapai-14300-rupiah-investasi-rumah-murah-di-depok.html          
    578     142   78       http://rumahdijual.com/depok/1013899-perumahan-sawangan-permai-luas-tnh-bngunan-mak-dengan-harga.html         
    579     270   166      http://rumahdijual.com/depok/1016153-aku-jual-rumah-adem-bejo-harga-ecoo-depok-kota.html                      
    580     147   70       http://rumahdijual.com/depok/1141477-rumah-jauh-dari-bising-dan-udara-segar.html                              
    580     135   120      http://rumahdijual.com/depok/1088897-rumah-siap-huni-di-perumahan-sukatani-permai-r21-0384-a.html             
    580     132   150      http://rumahdijual.com/depok/1070543-rumah-2-lantai-murah-siap-huni-pondok-sukatani-permai.html               
    580     130   70       http://rumahdijual.com/depok/1006245-di-jual-rumah-minimalis-siap-huni-di-kali-mulya.html                     
    580     130   70       http://rumahdijual.com/depok/1165054-rumah-cluster-harga-wafer.html                                           
    580     120   80       http://rumahdijual.com/depok/1092530-rumah-cluster-kota-depok.html                                            
    580     120   80       http://rumahdijual.com/depok/1097655-rumah-mewah-harga-murah.html                                             
    580     110   65       http://rumahdijual.com/depok/891518-rumah-strategis-model-minimalis-di-mampang-depok.html                     
    580     105   80       http://rumahdijual.com/depok/1070266-rumah-murah-lokasi-strategis-di-jantung-kota-depok-perumnas.html         
    580     104   80       http://rumahdijual.com/depok/1299087-dijual-rumah-cantik-bangunan-luas-harga-pas.html                         
    580     100   90       http://rumahdijual.com/depok/1051703-rumah-cantik-minimalis-di-jatimulya-depok-r21-0340-a.html                
    580     100   80       http://rumahdijual.com/depok/1175188-rumah-luas-dalam-cluster-dipitara-depok.html                             
    580     100   70       http://rumahdijual.com/depok/1270247-rumah-asri-sedang-bangun-di-raden-saleh-depok-r21.html                   
    585     229   150      http://rumahdijual.com/depok/1000759-rumah-di-cagar-alam-depok-1-a.html                                       
    585     128   70       http://rumahdijual.com/depok/1143851-rumah-strategis-di-cimanggis-housing-tapos-kota-depok.html               
    590     150   110      http://rumahdijual.com/depok/1117620-rumah-secondary-tanah-baru-depok.html                                    
    590     120   90       http://rumahdijual.com/depok/1304042-di-jual-rumah-asri-model-minimalis-sipa-huni-di.html                     
    590     115   80       http://rumahdijual.com/depok/927693-dijual-rumah-baru.html                                                    
    590     105   90       http://rumahdijual.com/depok/1063257-rumah-permata-depok.html                                                 
    590     105   90       http://rumahdijual.com/depok/608427-rumah-cantik-di-perumahan-permata-depok.html                              
    590     105   90       http://rumahdijual.com/depok/1286952-di-jual-rumah-cantik-suasana-alam-siap-huni-di.html                      
    595     128   114      http://rumahdijual.com/depok/1145171-rumah-mewah-murah-strategis-5-menit-ke-tol-cimanggis.html                
    595     117   85       http://rumahdijual.com/depok/963713-rumah-murah-di-cinangka-depok.html                                        
    595     100   75       http://rumahdijual.com/depok/1215578-rumah-di-jalan-mahakam-mampang-depok.html                                
    598     127   70       http://rumahdijual.com/depok/631482-baru-lb-70-m2-dan-lt-127m2-di-pondok.html                                 
    599     350   150      http://rumahdijual.com/depok/353621-rumah-dijual-di-pasirputih-sawangan-kota-depok.html                       
    599     120   70       http://rumahdijual.com/depok/1114793-rumah-murah-di-sawangan-permai.html                                      
    600     99    140      http://rumahdijual.com/depok/1207717-dijual-cepat-rumah-siap-huni-di-cimanggis-depok.html                     
    600     98    75       http://rumahdijual.com/depok/972204-kavling-jalan-merdeka-unit-terbatas-tinggal-1-unit.html                   
    600     400   120      http://rumahdijual.com/depok/1064129-rumah-tempat-tinggal-nyaman-dgn-tanah-luas-dan-lingkungan.html           
    600     270   100      http://rumahdijual.com/depok/1163246-rumah-baru-dijual-cepat-aman-dan-asri.html                               
    600     210   90       http://rumahdijual.com/depok/1107587-rumah-dijual-rumah-kampung-bertanah-luas-di-sawangan-depok.html          
    600     200   150      http://rumahdijual.com/depok/1050496-di-jual-rumah-kontrakan-4-pintu-dekat-jl-raya.html                       
    600     200   100      http://rumahdijual.com/depok/1011067-rumah-lt-lb-200-100-di-rangkapan-jaya-depok.html                         
    600     159   90       http://rumahdijual.com/depok/1064794-dijual-rumah.html                                                        
    600     150   80       http://rumahdijual.com/depok/1196688-cinangka-depok.html                                                      
    600     150   200      http://rumahdijual.com/depok/1306307-rumah-2-lantai-masuk-mobil-di-kalimulya-300-meter.html                   
    600     145   90       http://rumahdijual.com/depok/1126926-rumah-strategis-daerah-depok-murah.html                                  
    600     136   70       http://rumahdijual.com/depok/1262387-dijual-rumah-baru-siap-huni-lokasi-strategis-di-cilodong.html            
    600     135   141      http://rumahdijual.com/depok/979994-rumah-manis-di-putri-anggrek-mas-depok-jl-raya.html                       
    600     134   134      http://rumahdijual.com/depok/1009121-dijual-murah-kontrakkan-4-pintu-lokasi-strategis.html                    
    600     130   80       http://rumahdijual.com/depok/1016516-kavling-raden-saleh-hunian-megah-harga-menarik-hati.html                 
    600     130   70       http://rumahdijual.com/depok/1182940-rumah-luas-dalam-cluster-dipitara-depok.html                             
    600     130   65       http://rumahdijual.com/depok/973686-di-jual-rumah-murah-depok.html                                            
    600     130   65       http://rumahdijual.com/depok/884194-cari-rumah-baca-dulu-nih-tips-nya.html                                    
    600     130   100      http://rumahdijual.com/depok/818514-luas-tanah-130-m2-depok-maharaja.html                                     
    600     127   125      http://rumahdijual.com/depok/1166569-rumah-siap-huni-di-komplex-jatijajar-depok-jawa-barat.html               
    600     125   100      http://rumahdijual.com/depok/1173386-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html              
    600     121   80       http://rumahdijual.com/depok/915864-rumah-murah-di-beji-depok.html                                            
    600     121   100      http://rumahdijual.com/depok/1091091-perumahan-murah-di-cimanggis-r21-0386-a.html                             
    600     121   100      http://rumahdijual.com/depok/1290717-dijual-rumah-cluster-murah-di-limo-cinere.html                           
    600     120   70       http://rumahdijual.com/depok/1041307-rumah-nyaman-harga-teman.html                                            
    600     120   70       http://rumahdijual.com/depok/698761-kavling-h-sulaiman-rumah-cantik-hanya-3-unit-di.html                      
    600     120   160      http://rumahdijual.com/depok/878962-rumah-dijual-di-depok.html                                                
    600     120   100      http://rumahdijual.com/depok/1098564-rumah-hunian-cluster-di-pitara-pancoran-mas-kota-depok.html              
    600     120   100      http://rumahdijual.com/depok/1098503-hunian-cluster-strategis-di-pitara-pancoran-mas-kota-depok.html          
    600     120   100      http://rumahdijual.com/depok/1089704-cluster-modern-di-pitara-pancoran-mas-kota-depok.html                    
    600     120   100      http://rumahdijual.com/depok/1089946-rumah-cluster-jalan-pitara-raya-kota-depok.html                          
    600     120   100      http://rumahdijual.com/depok/1120073-hunian-dalam-cluster-one-gate-system-di-pitara-depok.html                
    600     120   100      http://rumahdijual.com/depok/1133352-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html             
    600     120   100      http://rumahdijual.com/depok/1133369-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html             
    600     120   100      http://rumahdijual.com/depok/1133414-rumah-cluster-pitara-pancoran-mas-kota-depok.html                        
    600     120   100      http://rumahdijual.com/depok/1133828-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html             
    600     120   100      http://rumahdijual.com/depok/1133855-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html             
    600     120   100      http://rumahdijual.com/depok/1109359-rumah-cluster-pancoran-mas-rangkapan-jaya-depok.html                     
    600     120   100      http://rumahdijual.com/depok/1102750-perumahan-griya-pratama-asri-pancoran-mas-depok.html                     
    600     120   100      http://rumahdijual.com/depok/1148317-perumahan-cluster-griya-pratama-asri-di-jalan-pitara-kota.html           
    600     120   100      http://rumahdijual.com/depok/1148322-one-gate-system.html                                                     
    600     120   100      http://rumahdijual.com/depok/1148621-hunian-nyaman-dan-asri.html                                              
    600     120   100      http://rumahdijual.com/depok/1092057-rumah-cluster-pitara-kota-depok.html                                     
    600     120   100      http://rumahdijual.com/depok/1092061-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html              
    600     120   100      http://rumahdijual.com/depok/1148610-griya-pratama-asri.html                                                  
    600     120   100      http://rumahdijual.com/depok/1150673-rumah-cluster-jalan-pitara-pancoran-mas-depok.html                       
    600     120   100      http://rumahdijual.com/depok/1150517-rumah-cluster-pitara-pancoran-mas-kota-depok.html                        
    600     120   100      http://rumahdijual.com/depok/1089680-hunian-cluster-pemukiman-nyaman-dan-asri-pitara-pancoran-mas.html        
    600     120   100      http://rumahdijual.com/depok/1133216-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html             
    600     120   100      http://rumahdijual.com/depok/1133203-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html             
    600     120   100      http://rumahdijual.com/depok/1138168-rumah-cluster-one-gate-system-pitara-pancoran-mas-depok.html             
    600     120   100      http://rumahdijual.com/depok/1133210-rumah-cluster-jalan-pitara-pancoran-mas-depok.html                       
    600     120   100      http://rumahdijual.com/depok/1133027-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html             
    600     120   100      http://rumahdijual.com/depok/1132961-hunian-cluster-griya-pratama-asri-di-pitara-depok.html                   
    600     120   100      http://rumahdijual.com/depok/1126678-rumah-cluster-one-gate-system.html                                       
    600     120   100      http://rumahdijual.com/depok/1100006-hunian-dalam-cluster-di-pitara-pancoran-mas-depok.html                   
    600     120   100      http://rumahdijual.com/depok/1131545-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html             
    600     120   100      http://rumahdijual.com/depok/1138161-perumahan-cluster-griya-pratama-asri.html                                
    600     120   100      http://rumahdijual.com/depok/1173218-rumah-depok.html                                                         
    600     117   85       http://rumahdijual.com/depok/1158180-dijual-rumah-murah-di-serua-bojongsari-depok.html                        
    600     115   200      http://rumahdijual.com/depok/836205-rumah-perumnas-gelatik-depok-1-a.html                                     
    600     110   80       http://rumahdijual.com/depok/1070207-di-jual-rumah-minimalis-dalem-kompleks.html                              
    600     110   65       http://rumahdijual.com/depok/996799-di-jual-rumah-cantik-di-belakang-global-islamic-school.html               
    600     110   110      http://rumahdijual.com/depok/979163-dijual-cepat-rumah-daerah-depok.html                                      
    600     110   110      http://rumahdijual.com/depok/756919-rumah-di-h-zakaria-tanah-baru.html                                        
    600     110   100      http://rumahdijual.com/depok/1107993-rumah-luas-full-granit-di-pitara-depok.html                              
    600     110   100      http://rumahdijual.com/depok/1107996-hunian-hook-dekat-jalan-raya-di-pitara-pancoran-mas.html                 
    600     108   70       http://rumahdijual.com/depok/1299718-di-jual-rumah-minimalis-siap-huni-lokasi-strategis-nempel.html           
    600     105   80       http://rumahdijual.com/depok/1231090-rumah-nyaman-dan-lokasi-strategis-di-depok.html                          
    600     105   65       http://rumahdijual.com/depok/927718-kavling-kemang-hunian-nyaman-dan-asri.html                                
    600     102   90       http://rumahdijual.com/depok/1103450-rumah-perumnas-lokasi-strategis.html                                     
    600     102   75       http://rumahdijual.com/depok/944089-hunian-asri-harga-terjangkau-kawasan-depok.html                           
    600     102   102      http://rumahdijual.com/depok/814128-dijual-rumah-di-depok-timur.html                                          
    600     100   86       http://rumahdijual.com/depok/987208-perumahan-lembah-hijau-tipe-86-100-di-mekarsari-depok.html                
    600     100   85       http://rumahdijual.com/depok/990881-dijual-rumah-second-di-cimanggis-layak-huni-dijual-cepat.html             
    600     100   80       http://rumahdijual.com/depok/921712-rumah-design-minimalis-terbaik-di-depok.html                              
    600     100   180      http://rumahdijual.com/depok/833294-rumah-murah-2-lantai-lembah-nirmala-2-mekarsari-depok.html                
    600     100   160      http://rumahdijual.com/depok/1241247-rumah-2-lantai-di-jual-di-sawangan.html                                  
    600     100   100      http://rumahdijual.com/depok/859807-rumah-sejuki-dan-asri-di-kavling-kencana.html
    


```python
selectExpensive(df, avg, unit)
```

    
    EXPENSIVE PRICE
    -----------------
    is when the price is above average: 550 (million IDR) but you only get land below average: 98 (square meters) and building below average: 64 (square meters).
    
    
    
    There are : 472  items that matched the EXPENSIVE category.
    
    price land building                                                                                                              url
    550     97   55       http://rumahdijual.com/depok/639317-rumah-aman-di-lingkungan-nyaman.html                                      
    550     96   54       http://rumahdijual.com/depok/997170-depok.html                                                                
    550     96   48       http://rumahdijual.com/depok/1189082-rumah-kpr-nyaman-dan-sari-di-tirtajaya-sukmajaya-depok.html              
    550     94   60       http://rumahdijual.com/depok/941823-rumah-siap-huni-depok-r21-0006-a.html                                     
    550     94   45       http://rumahdijual.com/depok/1301670-rumah-inden-3-bulan-masuk-mobil-di-raden-saleh.html                      
    550     93   54       http://rumahdijual.com/depok/739202-rumah-type-54-93-green-mutiara-jambore.html                               
    550     91   60       http://rumahdijual.com/depok/1268209-rumah-clusster-minimalis.html                                            
    550     90   60       http://rumahdijual.com/depok/1315204-rumah-di-permata-cimanggis-depok-jual-butuh.html                         
    550     90   50       http://rumahdijual.com/depok/1066542-rumah-cluster-nempel-grand-depok-city-gdc.html                           
    550     90   50       http://rumahdijual.com/depok/619082-dijual-14-unit-rumah-baru.html                                            
    550     90   50       http://rumahdijual.com/depok/981592-hunian-ekslusif-nuansa-orange-di-pinggir-jalan-raya-sawangan.html         
    550     90   45       http://rumahdijual.com/depok/1169339-permata-cimanggis-depok-dekat-tol.html                                   
    550     90   45       http://rumahdijual.com/depok/868963-rumah-di-depok-kavling-ui-strategis-deket-stasiun.html                    
    550     90   45       http://rumahdijual.com/depok/509204-pandawa-2-rumah-cluster-exclusive-mampang-pancoran-depok.html             
    550     90   45       http://rumahdijual.com/depok/509187-rumah-cluster-minimalis-strategis-mampang-depok.html                      
    550     90   43       http://rumahdijual.com/depok/916563-rumah-di-sawangan-residence-ideal-550-juta.html                           
    550     90   30       http://rumahdijual.com/depok/1059036-rumah-dijual-siap-huni-bukit-rivaria-sawangan-depok.html                 
    550     89   45       http://rumahdijual.com/depok/901054-alexandria-purple-harga-terjangkau.html                                   
    550     88   60       http://rumahdijual.com/depok/945535-rumah-menarik-harga-cantik.html                                           
    550     88   55       http://rumahdijual.com/depok/833987-rumah-tingkat-suasana-asri-dekat-grand-depok-city.html                    
    550     88   45       http://rumahdijual.com/depok/1240434-rumah-dijual-cepat.html                                                  
    550     87   52       http://rumahdijual.com/depok/745731-di-jual-rumah-cantik-exclusive-raden-saleh-depok-105-a.html               
    550     87   50       http://rumahdijual.com/depok/1085947-cluster-minimalis-harga-terjangkau.html                                  
    550     86   48       http://rumahdijual.com/depok/1240723-dijual-rumah-murah.html                                                  
    550     86   45       http://rumahdijual.com/depok/1307139-perumahan-murah-dekat-ui-harga-ekonomisdan-strategis.html                
    550     86   39       http://rumahdijual.com/depok/1273529-rumah-idaman-cluster-jayana-valley.html                                  
    550     86   39       http://rumahdijual.com/depok/1273582-rumah-idaman-cluster-jayana-valley.html                                  
    550     85   55       http://rumahdijual.com/depok/996786-di-jual-rumah-baru-siap-huni-tanpa-renovasi-di.html                       
    550     85   53       http://rumahdijual.com/depok/1006392-rumah-di-greenland-sawangan-depok.html                                   
    550     85   52       http://rumahdijual.com/depok/1282224-hunian-strategis-harga-minimalis-di-sawangan-depok.html                  
    550     85   45       http://rumahdijual.com/depok/1070639-rumah-murah-di-alam-studio-tvri-depok.html                               
    550     85   40       http://rumahdijual.com/depok/1312654-cluster-siap-huni-di-cinere-depok-r21-0499-a.html                        
    550     84   60       http://rumahdijual.com/depok/901484-rumah-dijual-cepat.html                                                   
    550     84   60       http://rumahdijual.com/depok/953627-rumah-murah-beji-depok.html                                               
    550     84   60       http://rumahdijual.com/depok/937124-rumah-cluster-strategis-ekonomis-dekat-univ-indonesia.html                
    550     84   56       http://rumahdijual.com/depok/1306904-rumah-dijual-over-kredit-grand-depok-city-cluster-gmm.html               
    550     84   54       http://rumahdijual.com/depok/999665-di-jual-rumah-baru-siap-huni-di-ksu-depok.html                            
    550     84   54       http://rumahdijual.com/depok/903566-rumah-murah-spesifikasi-sangat-menguntungkan-buktikan.html                
    550     84   54       http://rumahdijual.com/depok/973124-cinere-valley-view.html                                                   
    550     84   50       http://rumahdijual.com/depok/1237609-rumah-strategis-di-taman-bumi-agung-residence-sawangan-depok.html        
    550     84   50       http://rumahdijual.com/depok/825980-cluster-exlusive-bebas-biaya-surat2-shm-bonus-ac-tlp.html                 
    550     84   50       http://rumahdijual.com/depok/929650-cluster-exlusive-bebas-biaya-surat2-shm-bonus-ac-tlp.html                 
    550     84   48       http://rumahdijual.com/depok/886888-perumahan-griya-pinus-tanah-baru-depok.html                               
    550     84   45       http://rumahdijual.com/depok/1276709-rumah-baru-di-beji-kukusan-depok-cluster-model-minimalis.html            
    550     84   45       http://rumahdijual.com/depok/1078776-jual-rumahtype-45-harga-550-akses-sangat-mudah.html                      
    550     84   45       http://rumahdijual.com/depok/1307357-cluster-di-tanah-baru-depok-harga-paling-ringan.html                     
    550     84   45       http://rumahdijual.com/depok/1276568-yang-lagi-cari-cari-rumah-di-beji-depok-yuks.html                        
    550     84   45       http://rumahdijual.com/depok/1309525-ayo-jangan-salah-pilih-rumah-yang-ini-sudah-paling.html                  
    550     84   40       http://rumahdijual.com/depok/1094686-rumah-bernuansa-taman-dan-strategis.html                                 
    550     83   55       http://rumahdijual.com/depok/1047043-rumah-cluster-di-tanah-baru.html                                         
    550     83   55       http://rumahdijual.com/depok/754502-rumah-cluster-di-tanah-baru-10-menit-ke-stasiun.html                      
    550     83   45       http://rumahdijual.com/depok/1293791-cluster-cantik-500jutaan-15-menit-ke-stasiun-depok-baru.html             
    550     82   45       http://rumahdijual.com/depok/1241404-rumah-cantik-didalam-perumahan-full-kayu-jati.html                       
    550     82   45       http://rumahdijual.com/depok/1274597-dijual-cepat-rumah-di-jalan-merdeka-sukmajaya-depok.html                 
    550     81   55       http://rumahdijual.com/depok/1077775-rumah-cantik-di-cluster-bakti-indah-depok.html                           
    550     81   55       http://rumahdijual.com/depok/1089722-cluster-bakti-indah.html                                                 
    550     81   50       http://rumahdijual.com/depok/1062867-rumah-cluster-minimalis-bakti-indah-di-depok-cimanggis-0822-a.html       
    550     81   50       http://rumahdijual.com/depok/1137836-rumah-dijual-depok-kavling-bakti-indah-tapos.html                        
    550     81   50       http://rumahdijual.com/depok/1156909-rumah-cluster-pekapuran-depok.html                                       
    550     80   60       http://rumahdijual.com/depok/1293089-perumahan-siaphuni-di-tanah-baru-depok-r21-0479-a.html                   
    550     80   60       http://rumahdijual.com/depok/1292657-cluster-di-tanah-baru-depok-r21-478-a.html                               
    550     80   55       http://rumahdijual.com/depok/989389-cluster-merpati-garden-sukatani-depok.html                                
    550     80   50       http://rumahdijual.com/depok/898240-raden-sanim-rumah-ideal-tenang-aman.html                                  
    550     80   45       http://rumahdijual.com/depok/1253864-rumah-bagus-di-perumnas-beji-tanah-baru-depok.html                       
    550     80   45       http://rumahdijual.com/depok/1299964-rumah-minimalis-di-tanah-baru-beji.html                                  
    550     80   45       http://rumahdijual.com/depok/1300934-cluster-minimalis-tanah-baru-dekat-beji-murah-rh325.html                 
    550     80   45       http://rumahdijual.com/depok/1275441-rumah-bagus-harga-minimalis-di-tanah-baru.html                           
    550     80   45       http://rumahdijual.com/depok/569708-rumah-minimalis-dalam-cluster-di-tanah-baru-beji-depok.html               
    550     80   45       http://rumahdijual.com/depok/1289451-rumah-murah-di-depok.html                                                
    550     80   45       http://rumahdijual.com/depok/1291257-dijual-rumah-murah-di-depok.html                                         
    550     80   45       http://rumahdijual.com/depok/1307336-rumah-minimalis-beji-depok.html                                          
    550     80   45       http://rumahdijual.com/depok/1290493-perumahan-unik-dekat-ke-jalan-raya-tanah-baru-beji.html                  
    550     80   45       http://rumahdijual.com/depok/796436-momien-residence-cluster-one-gate-harga-terjangkau-dp-di.html             
    550     80   45       http://rumahdijual.com/depok/1314295-dijual-rumah-di-tanah-baru-beji-depok-include-biaya.html                 
    550     80   45       http://rumahdijual.com/depok/1305351-cluster-dekat-stasiun-di-depok.html                                      
    550     80   45       http://rumahdijual.com/depok/1301310-rumah-dijual-di-beji-tanah-baru-depok-bisa-kpr.html                      
    550     80   45       http://rumahdijual.com/depok/1287606-ayo-wujudkan-mimpi-anda-untuk-memiliki-rumah-di-beji.html                
    550     80   45       http://rumahdijual.com/depok/1300634-rumah-dijual-di-tanah-baru-beji-view-indah-berasa.html                   
    550     80   45       http://rumahdijual.com/depok/1312600-cluster-murah-di-tanah-baru-depok.html                                   
    550     80   45       http://rumahdijual.com/depok/879915-cluster-lokasi-tanah-baru-beji-depok.html                                 
    550     80   45       http://rumahdijual.com/depok/922403-rumah-murah-kualitas-bagus-di-tanah-baru-beji-depok.html                  
    550     80   45       http://rumahdijual.com/depok/1310726-rumah-murah-di-depok-tanah-baru-beji-harga-murah.html                    
    550     80   45       http://rumahdijual.com/depok/1289391-rumah-dijual-di-kukusan-beji-dekat-stasiun-cluster-baru.html             
    550     80   45       http://rumahdijual.com/depok/1301101-cluster-momien-residence-lokasi-strategis-di-tanah-baru-beji.html        
    550     80   45       http://rumahdijual.com/depok/872341-momien-residence-cluster-idaman-harga-terjangkau-dp-ringgan-selangkah.html
    550     80   45       http://rumahdijual.com/depok/1307963-ready-stock-cluster-500jutaan-di-tanah-baru-pinggir-jalan.html           
    550     80   45       http://rumahdijual.com/depok/1307954-ready-stock-cluster-menawan-di-tanah-baru-beji.html                      
    550     80   45       http://rumahdijual.com/depok/1289412-rumah-dijual-murah-gratis-kitchen-set-torn-air-di.html                   
    550     80   45       http://rumahdijual.com/depok/1283951-rumah-cluster-termurah-di-tanah-baru-depok.html                          
    550     80   45       http://rumahdijual.com/depok/1305769-rumah-minimalis.html                                                     
    550     80   45       http://rumahdijual.com/depok/1306277-hunian-pinggir-jalan-tanah-baru-harga-terjangkau.html                    
    550     80   45       http://rumahdijual.com/depok/1286647-rumah-bagus-di-tanah-baru-depok.html                                     
    550     80   45       http://rumahdijual.com/depok/1307850-rumah-murah-di-beji-depok.html                                           
    550     80   45       http://rumahdijual.com/depok/916790-momien-residence-cluster-harga-irit-dp-ringan-free-legalitas.html         
    550     80   45       http://rumahdijual.com/depok/1307969-cantik-harga-500jutaan-di-tanah-baru-di-beji-depok.html                  
    550     80   45       http://rumahdijual.com/depok/1307981-terjual-6-unit-dalam-1-bulan-cluster-murah-di.html                       
    550     80   45       http://rumahdijual.com/depok/1307918-rumah-murah-di-depok-dekat-stasiun.html                                  
    550     80   45       http://rumahdijual.com/depok/1302254-rumah-murah-type-minimalis-di-tanah-baru-beji-depok.html                 
    550     80   45       http://rumahdijual.com/depok/1300905-cluster-dekat-stasiun-di-beji-depok.html                                 
    550     80   45       http://rumahdijual.com/depok/1300894-cluster-menarik-di-beji-depok.html                                       
    550     80   45       http://rumahdijual.com/depok/1300880-rumah-murah-di-beji-depok.html                                           
    550     80   45       http://rumahdijual.com/depok/1299490-rumah-minimalis-di-tanah-baru-beji-rmh013.html                           
    550     80   36       http://rumahdijual.com/depok/1083378-dijual-rumah-dekat-ciputat-dan-jakarta-selatan.html                      
    550     78   48       http://rumahdijual.com/depok/1117409-rumah-kokoh-full-bata-merah-one-gate-asri-di.html                        
    550     78   42       http://rumahdijual.com/depok/893823-dijual-cepat-rumah-murah-harga-550juta-lokasi-strategis.html              
    550     78   36       http://rumahdijual.com/depok/1054058-rumah-dijual-siap-huni-di-jalan-ksu-kalimulya-kota.html                  
    550     77   55       http://rumahdijual.com/depok/800222-town-house-green-lite-modern-concept.html                                 
    550     77   50       http://rumahdijual.com/depok/1296886-jual-khilaf-siapa-cepat-dia-dapat-lokasi-ok-kpr.html                     
    550     77   50       http://rumahdijual.com/depok/1291392-jual-khilkaf-spek-ok-lokasi-strategis-kpr-dp-cukup.html                  
    550     76   54       http://rumahdijual.com/depok/1131433-rumah-cantik-dan-menarik-harga-bagus-di-sawangan.html                    
    550     76   48       http://rumahdijual.com/depok/1268449-rimah-minimalis-dekat-tole-iskandar-depok.html                           
    550     75   50       http://rumahdijual.com/depok/1062494-rumah-di-maharaja-depok.html                                             
    550     75   48       http://rumahdijual.com/depok/894096-manis-minimalis-dan-murah-cluster-120-meter-dr-angkot.html                
    550     75   45       http://rumahdijual.com/depok/1156724-cluster-pi-residence.html                                                
    550     75   39       http://rumahdijual.com/depok/851290-rumah-mungil-permata-arcadia-cimanggis-depok.html                         
    550     72   60       http://rumahdijual.com/depok/741128-di-jual-rumah-bagus-di-permata-regency-depok-91-a.html                    
    550     72   60       http://rumahdijual.com/depok/1194320-rumah-di-jual-di-klapa-2-depok.html                                      
    550     72   60       http://rumahdijual.com/depok/1300755-rumah-keren-harga-beken.html                                             
    550     72   60       http://rumahdijual.com/depok/1189078-rumah-di-jual-untuk-investasi-di-daerah-cimanggis-depok.html             
    550     72   60       http://rumahdijual.com/depok/1126469-rumah-dijual-di-kelapa-dua-depok-di-dalam-cluster.html                   
    550     72   60       http://rumahdijual.com/depok/1225329-rumah-dijual-bu-lokasi-di-dalam-cluster-dikelapa-dua.html                
    550     72   60       http://rumahdijual.com/depok/1189125-di-jual-cepat-rumah-di-kelapa-dua-depok.html                             
    550     72   60       http://rumahdijual.com/depok/1187039-rumah-dijual-di-kelapa-dua-depok-lokasi-strategis-bebas.html             
    550     72   60       http://rumahdijual.com/depok/1144808-cari-rumah-murah-di-cluster-kelapa-dua-cimanggis-depok.html              
    550     72   60       http://rumahdijual.com/depok/1113894-bu-rumah-strategis-di-cimanggis-depok.html                               
    550     72   60       http://rumahdijual.com/depok/1101888-rumah-dijual-di-cluster-kelapa-dua-cimanggis-depok-550-a.html            
    550     72   54       http://rumahdijual.com/depok/994854-tanpa-dp-bonus-taman-hanya-10-unit.html                                   
    550     72   50       http://rumahdijual.com/depok/1105227-perumahan-depok-timur-lokasi-strategis-15-mnt-stasiun-terminal.html      
    550     72   50       http://rumahdijual.com/depok/1105253-perumahan-depok-timur-lokasi-strategis-15-mnt-stasiun-terminal.html      
    550     72   50       http://rumahdijual.com/depok/947808-cluster-strategis-griya-taman-tiga-putra.html                             
    550     72   50       http://rumahdijual.com/depok/1299215-rumah-di-grand-depok-city.html                                           
    550     72   48       http://rumahdijual.com/depok/774768-cluster-nempel-jaksel-dkt-kampus-ui-depok.html                            
    550     72   48       http://rumahdijual.com/depok/1293032-rumah-cantik-siap-huni-48-72-permata-depok-br.html                       
    550     72   45       http://rumahdijual.com/depok/1042682-rumah-cantik-siap-huni-di-sektor-gardenia-grand-depok.html               
    550     72   40       http://rumahdijual.com/depok/1236068-grand-pesona.html                                                        
    550     72   40       http://rumahdijual.com/depok/1126952-rumah-depok-dijual-daerah-mampang.html                                   
    550     72   36       http://rumahdijual.com/depok/1275593-rumah-di-gdr-depok.html                                                  
    550     72   36       http://rumahdijual.com/depok/1124232-rumah-murah-di-depok-pancoran-mas-depok.html                             
    550     72   36       http://rumahdijual.com/depok/1161611-rumah-minimalis-free-kitchen-set-di-perumahan-vila-mutiara.html          
    550     72   36       http://rumahdijual.com/depok/1312527-cluster-cantik-di-cinere-r21-0498-a.html                                 
    550     70   60       http://rumahdijual.com/depok/1011619-rumah-dijual-murah-di-grand-depok-city-sektor-melati.html                
    550     70   56       http://rumahdijual.com/depok/834372-di-mekarsari-cimanggis-depok.html                                         
    550     70   55       http://rumahdijual.com/depok/1226893-rumah-baru-dekat-matoa-golf-samping-jln-raya-kafi.html                   
    550     66   38       http://rumahdijual.com/depok/888003-rumah-dijual-cluster-minimalis-dekat-dengan-rencana-tol.html              
    550     60   49       http://rumahdijual.com/depok/1280718-rumah-cantik-di-tanah-baru-depok-r21-0471-a.html                         
    550     6    38       http://rumahdijual.com/depok/1312000-dijual-bu-rumah-di-perum-payung-mas-residence.html                       
    551     72   51       http://rumahdijual.com/depok/823400-rumah-manis-siap-huni-tanah-baru-depok-kpr-murah.html                     
    551     72   45       http://rumahdijual.com/depok/581067-green-ambara-gardenia-cinere.html                                         
    552     89   36       http://rumahdijual.com/depok/1212917-jual-rumah-bonus-mobil-sawangan-depok.html                               
    554     84   50       http://rumahdijual.com/depok/812977-cluster-exlusive-dp-suka-suka-bebas-biaya-surat2-shm.html                 
    555     77   40       http://rumahdijual.com/depok/1076418-rumah-siap-huni-depok.html                                               
    555     75   55       http://rumahdijual.com/depok/801909-rumah-sawangan-primadona-dikelasnya-town-house-green-lite.html            
    555     72   40       http://rumahdijual.com/depok/1183119-new-grand-pesona.html                                                    
    557     91   36       http://rumahdijual.com/depok/1279359-perumahan-di-gdc-depok-bisa-desain-bentuk-layout-rumah.html              
    557     91   36       http://rumahdijual.com/depok/1283830-rumah-baru-harga-murah-dp-bisa-dicicil-di-kota.html                      
    557     84   50       http://rumahdijual.com/depok/1241490-perumahan-murah-di-lokasi-strategis-di-pancoran-mas-depok.html           
    557     84   50       http://rumahdijual.com/depok/1257359-dijual-rumah-cluster-masih-hangat-ready-stock-dan-baru.html              
    557     75   50       http://rumahdijual.com/depok/1309587-best-invest-best-location.html                                           
    557     72   40       http://rumahdijual.com/depok/1121000-dijual-rumah-murah-lokasi-strategis-di-pancoran-mas-depok.html           
    557     72   40       http://rumahdijual.com/depok/1057371-dijual-rumah-didepok-kpr-atau-cash-lokasi-strategis-dekat.html           
    557     72   40       http://rumahdijual.com/depok/1050989-rumah-murah-di-depok-mampang-pancoran-mas-dekat-margonda.html            
    557     72   40       http://rumahdijual.com/depok/1048308-cluster-di-pancoran-mas-mampang-depok-ada-1-dan.html                     
    557     72   40       http://rumahdijual.com/depok/1120786-dijual-rumah-murah-di-pancoran-mas-depok.html                            
    557     72   40       http://rumahdijual.com/depok/1071041-rumah-murah-di-perkotaan.html                                            
    557     72   40       http://rumahdijual.com/depok/1070584-rumah-dijual-dipancoran-depok.html                                       
    557     72   40       http://rumahdijual.com/depok/1248681-rumah-minimalis-harga-murah-di-pancoran-mas-depok.html                   
    557     72   40       http://rumahdijual.com/depok/927307-graha-mampang-mas-pancoran-depok-lokasi-strategis-dekat-margonda.html     
    557     72   40       http://rumahdijual.com/depok/1229615-perumahan-murah-di-lokasi-strategis-di-pancoran-mas-depok.html           
    557     72   40       http://rumahdijual.com/depok/1248491-rumah-murah-minimalis-di-kota-depok-lokasi-sangat-strategis.html         
    557     72   40       http://rumahdijual.com/depok/1235621-perumahan-murah-disawangan-depok.html                                    
    557     72   40       http://rumahdijual.com/depok/1052103-perumahan-murah-di-depok-2-lantai-dan-1-lantai.html                      
    557     72   40       http://rumahdijual.com/depok/1124122-rumah-murah-di-lokasi-strategis-di-pancoran-mas-depok.html               
    557     72   40       http://rumahdijual.com/depok/1233397-prumahan-murah-di-pancoran-depok.html                                    
    557     72   40       http://rumahdijual.com/depok/1287488-rumah-murah-depok-500-juta.html                                          
    557     72   40       http://rumahdijual.com/depok/921283-di-jual-rumah-cluster-mampang-mas-depok-harga-masih.html                  
    557     72   40       http://rumahdijual.com/depok/1158681-perumahan-murah-di-depok.html                                            
    557     72   40       http://rumahdijual.com/depok/1200788-perumahan-murah-di-lokasi-strategis-di-pancoran-mas-depok.html           
    557     72   40       http://rumahdijual.com/depok/1246719-rumah-minimalis-fasilitas-kolam-renang-di-depok.html                     
    557     72   40       http://rumahdijual.com/depok/1230808-rumah-murah-di-pancoran-mas-depok.html                                   
    557     72   40       http://rumahdijual.com/depok/1313295-rumah-depok-akses-ok-banget.html                                         
    557     72   40       http://rumahdijual.com/depok/1244714-rumah-cluster-murah-di-depok.html                                        
    557     72   40       http://rumahdijual.com/depok/1157909-perumahan-murah-di-lokasi-strategis-di-pancoran-mas-depok.html           
    557     70   40       http://rumahdijual.com/depok/1297037-satu-satunya-hunian-asri-dan-nyaman-di-kelasnya-harga500an.html          
    560     95   45       http://rumahdijual.com/depok/1099322-hunian-modern-dan-minimalis-harga-bersaing.html                          
    560     94   43       http://rumahdijual.com/depok/999949-rumah-murah-dan-strategis-mampang-indah-depok.html                        
    560     92   40       http://rumahdijual.com/depok/964626-taman-bumi-agung-residence-sawangan-depok.html                            
    560     88   36       http://rumahdijual.com/depok/1258472-isana-griya-hunian-eksklusif-asri-dan-tenang.html                        
    560     84   63       http://rumahdijual.com/depok/1113834-rumah-di-cipayung-depok.html                                             
    560     84   60       http://rumahdijual.com/depok/667336-rumah-baru-merayu.html                                                    
    560     80   46       http://rumahdijual.com/depok/1205213-rumah-murah-di-depok-10-menit-ke-stasiun.html                            
    560     80   45       http://rumahdijual.com/depok/898901-rumah-cantik-siap-huni-dan-kpr-cluster-120-meter.html                     
    560     80   45       http://rumahdijual.com/depok/822249-rumah-manis-minimalis-cluster-120-m-dr-jalur-angkot.html                  
    560     80   45       http://rumahdijual.com/depok/823381-rumah-manis-minimalis-cluster-120-m-dr-jalur-angkot.html                  
    560     79   61       http://rumahdijual.com/depok/1107748-cluster-akses-2-mobil-siap-huni-100mtr-ke-jalan.html                     
    560     79   50       http://rumahdijual.com/depok/1170496-rumah-murah-cluster-kukusan-dekat-pintu-tol-cijago.html                  
    561     75   50       http://rumahdijual.com/depok/1309569-best-invest-best-location.html                                           
    561     75   45       http://rumahdijual.com/depok/767568-cluster-barcelona-rumah-aman-di-lingkungan-nyaman.html                    
    561     72   45       http://rumahdijual.com/depok/941575-rumah-cinere-depok.html                                                   
    562     83   47       http://rumahdijual.com/depok/284490-perumahan-di-depok-gasari-residence-500m-ke-tol-cijago.html               
    562     83   45       http://rumahdijual.com/depok/1289478-rumah-minimalis-di-beji-depok-free-kitchen-set-torn.html                 
    562     83   45       http://rumahdijual.com/depok/1292866-dijual-rumah-baru-dalam-cluster-free-kitchen-set-dan.html                
    562     81   45       http://rumahdijual.com/depok/1307378-perumahan-cendana-regency.html                                           
    562     81   45       http://rumahdijual.com/depok/1225264-rumah-di-sawangan-depok.html                                             
    562     81   45       http://rumahdijual.com/depok/1240667-jual-cluster-akasia-type-45-81-cendana-regency-h.html                    
    562     81   45       http://rumahdijual.com/depok/1273124-cendana-regency-h-city-sawangan-hk-realtindo.html                        
    562     81   45       http://rumahdijual.com/depok/1266191-rumah-nyaman-dan-menyenangkan.html                                       
    562     81   45       http://rumahdijual.com/depok/1285111-di-jual-perumahan-harga-perdana-lokasi-prime-di-depok.html               
    562     81   45       http://rumahdijual.com/depok/1263297-cendana-regency-sawangan-hk-realtindo.html                               
    562     81   45       http://rumahdijual.com/depok/1263236-cendana-regency-sawangan.html                                            
    563     92   58       http://rumahdijual.com/depok/694207-hunian-nyaman-strategis-unit-terbatas-dapatkan-bonus-full-furnished.html  
    565     91   60       http://rumahdijual.com/depok/1127776-rumah-murah-di-dekat-gdc-depok.html                                      
    565     90   42       http://rumahdijual.com/depok/1214375-puri-arsana-sawangan-bojongsari-depok-jawa-barat.html                    
    565     84   45       http://rumahdijual.com/depok/1117847-cluster-siap-huni-di-kalimulya-r21-0403-a.html                           
    565     81   60       http://rumahdijual.com/depok/1311471-rumah-baru-minimalis-yg-nyaman-di-beji-depok-tidak.html                  
    565     77   55       http://rumahdijual.com/depok/824538-rumah-swaangan-lokasi-strategis-murah.html                                
    565     77   55       http://rumahdijual.com/depok/888731-mau-invest-rumah-sawangan-di-greenlite-town-house-saja.html               
    565     77   55       http://rumahdijual.com/depok/804555-rumah-perumahan-murah-di-sawangan-depok.html                              
    565     77   55       http://rumahdijual.com/depok/828564-green-lite-town-house-sawangan-depok.html                                 
    565     77   55       http://rumahdijual.com/depok/826107-rumah-dijual-murah-di-sawangan-depok.html                                 
    565     77   55       http://rumahdijual.com/depok/871427-rumah-sawangan-lokasi-super-nyaman-siap-huni-lokasi-strategis.html        
    565     77   55       http://rumahdijual.com/depok/795322-town-house-green-lite-sawangan-rumah-murah-depok.html                     
    565     77   55       http://rumahdijual.com/depok/873445-rumah-sawangan-greenlite-townhouse-lokasi-strategis-harga-perdana.html    
    565     77   55       http://rumahdijual.com/depok/793887-rumah-murah-di-sawangan-depok-cluster-baru.html                           
    565     77   55       http://rumahdijual.com/depok/795903-perumahan-baru-green-lite-town-house-depok-sawangan-harga.html            
    565     77   55       http://rumahdijual.com/depok/795155-rumah-strategis-depok-dekat-masjid-kubah-rencana-tol-cinere.html          
    565     77   55       http://rumahdijual.com/depok/805562-town-house-di-sawangan-depok-harga-murah.html                             
    565     75   50       http://rumahdijual.com/depok/822230-rumah-minimalis-cluster-tanah-baru-depok-120-m-dr.html                    
    565     74   48       http://rumahdijual.com/depok/1279996-hunian-ready-stock-spek-bagus-harga-miris-di-beji.html                   
    565     74   48       http://rumahdijual.com/depok/985440-hunian-asri-harga-miris-lokasi-strategis-di-tanah-baru.html               
    565     74   48       http://rumahdijual.com/depok/874725-cluster-strategis-di-tanah-baru.html                                      
    565     74   48       http://rumahdijual.com/depok/1066355-cluster-tanah-baru-beji-depok.html                                       
    565     74   48       http://rumahdijual.com/depok/1279925-cluster-terbaik-ditanah-baru-ready-stock-harga-terjamgkau.html           
    565     74   48       http://rumahdijual.com/depok/799445-rumah-minimalis-lokasi-strategis-kota-depok.html                          
    565     74   48       http://rumahdijual.com/depok/1226203-berlian-tahab-3-hunian-nyaman-harga-teman.html                           
    565     74   48       http://rumahdijual.com/depok/939036-cluster-berlian-investasi-cantik-harga-iriittt.html                       
    565     74   48       http://rumahdijual.com/depok/1234134-cluster-minimalis-strategis-depok-selangkah-jaksel-10-menit-stasiun.html 
    565     74   48       http://rumahdijual.com/depok/839989-hunian-strategis-harga-bersahabat-di-tanah-baru.html                      
    565     74   48       http://rumahdijual.com/depok/606957-cluster-elit-harga-iriiiitt-dekat-kampus-ui-depok.html                    
    565     74   48       http://rumahdijual.com/depok/1269706-new-berlian-lokasi-terdepan-kpr-dp-ringan-proses-gak.html                
    565     74   48       http://rumahdijual.com/depok/803089-rumah-idaman-keluarga-anda.html                                           
    565     74   48       http://rumahdijual.com/depok/809263-cluster-minimalis-nempel-kampus-ui-kota-depok.html                        
    565     74   45       http://rumahdijual.com/depok/911751-cluster-keren-free-legallitas-lokasi-selangkah-ke-jaksel.html             
    565     73   55       http://rumahdijual.com/depok/897276-rumah-murah-di-sawangan.html                                              
    565     73   55       http://rumahdijual.com/depok/790433-green-lite-town-house-depok-hunia-ekslusive.html                          
    565     73   55       http://rumahdijual.com/depok/790951-rumah-murah-lokasi-strategis-masih-gress-belum-di-ketahui.html            
    565     73   55       http://rumahdijual.com/depok/800203-town-house-green-lite-modern-concept.html                                 
    565     73   55       http://rumahdijual.com/depok/793745-green-lite-townhouse-murah-sawangan-depok.html                            
    565     72   48       http://rumahdijual.com/depok/895046-rumah-baru-cluster-nyaman-di-tanah-baru-depok-jalan.html                  
    565     72   45       http://rumahdijual.com/depok/750987-rumah-manis-minimalis-bisa-kpr-murah-di-tanah-baru.html                   
    565     72   36       http://rumahdijual.com/depok/274081-dijual-rumah-ready-dekat-stasiun-dan-margonda-depok.html                  
    566     95   45       http://rumahdijual.com/depok/1236057-hunian-di-cluster-besar-bisa-kpr-dp-ringan-ready.html                    
    566     86   36       http://rumahdijual.com/depok/796131-rumah-depok-akses-strategis.html                                          
    568     72   33       http://rumahdijual.com/depok/1230713-cluster-exclusive-di-jalan-raya-bogor-depok.html                         
    568     72   33       http://rumahdijual.com/depok/1230933-rumah-minimalis-di-kota-depok-bisa-tanpa-dp-ada.html                     
    569     90   45       http://rumahdijual.com/depok/774645-di-jual-rumah-di-delavender-town-house-cibinong-157-a.html                
    569     85   30       http://rumahdijual.com/depok/1055389-rumah-baru-bagus-untuk-tinggal-dan-investasi.html                        
    570     96   57       http://rumahdijual.com/depok/1017136-rumah-minimalis-dijual-murah-di-depok.html                               
    570     96   45       http://rumahdijual.com/depok/1106745-rumah-di-dalam-cluster-gdc.html                                          
    570     90   54       http://rumahdijual.com/depok/1122055-rumah-2nd-tipe-54-90-kpr-rp-570jt-nego.html                              
    570     90   45       http://rumahdijual.com/depok/1051220-di-jual-rumah-minimalis-di-perumahan-studio-alam.html                    
    570     86   60       http://rumahdijual.com/depok/1133305-rumah-baru-harga-bagus.html                                              
    570     86   50       http://rumahdijual.com/depok/593116-rumaha-minimalsi-di-dalam-komplek-depok-tanah-baru.html                   
    570     84   47       http://rumahdijual.com/depok/1050468-rumah-cluster-nempel-dengan-jakarta-selatan.html                         
    570     84   47       http://rumahdijual.com/depok/1040875-perumahan-di-tanah-baru-dengan-harga-terjangkau.html                     
    570     84   47       http://rumahdijual.com/depok/1247747-rumah-baru-di-tanah-baru-lingkungan-tenang-ada-akses.html                
    570     84   45       http://rumahdijual.com/depok/848907-6-unit-rumah-semi-cluster-di-tanah-baru-100-a.html                        
    570     84   45       http://rumahdijual.com/depok/1063165-rumah-cluster-baru-dekat-lap-golf-matoa-di-tanah.html                    
    570     84   38       http://rumahdijual.com/depok/820317-cluster-amaryllis-garden-r21-0228-a.html                                  
    570     82   50       http://rumahdijual.com/depok/1271920-rumah-idaman-di-kota-depok.html                                          
    570     81   45       http://rumahdijual.com/depok/1306808-rumah-minimalis-di-tanah-baru-depok.html                                 
    570     80   47       http://rumahdijual.com/depok/1026002-rumah-strategis-cimanggis-depok.html                                     
    570     75   50       http://rumahdijual.com/depok/745527-rumah-manis-minimalis-cluster-tanah-baru-depok-120-m.html                 
    570     75   50       http://rumahdijual.com/depok/745577-rumah-manis-minimalis-cluster-tanah-baru-depok-120-m.html                 
    574     86   45       http://rumahdijual.com/depok/1305361-cluster-cantik-di-depok.html                                             
    574     86   45       http://rumahdijual.com/depok/1300899-hunian-strategis-dekat-kampus-ui-depok.html                              
    574     86   45       http://rumahdijual.com/depok/1299985-rumah-murah-berkualitas-di-beji-tanah-baru-depok.html                    
    574     86   45       http://rumahdijual.com/depok/1286673-rumah-bagus-harga-miring-di-tanah-baru-depok.html                        
    574     86   45       http://rumahdijual.com/depok/1300887-rumah-strategis-di-beji-depok.html                                       
    574     86   45       http://rumahdijual.com/depok/1292887-rumah-dijual-gaya-minimalis-di-depok-free-kitchen-torn.html              
    575     92   58       http://rumahdijual.com/depok/745720-di-jual-rumah-exclusif-raden-saleh-depok-103-a.html                       
    575     92   45       http://rumahdijual.com/depok/842878-cluster-eight-townhouse.html                                              
    575     91   40       http://rumahdijual.com/depok/857144-rumah-cantik-harga-pas-pasan-di-depok.html                                
    575     90   54       http://rumahdijual.com/depok/914252-sara-house-rumah-yang-nyaman-tanpa-bising-pondok-cabe.html                
    575     90   54       http://rumahdijual.com/depok/772759-rumah-baru-cantik-siap-huni-di-cinangka.html                              
    575     90   50       http://rumahdijual.com/depok/49033-rumah-murah-di-pondok-cabe.html                                            
    575     90   50       http://rumahdijual.com/depok/1213741-nine-resiidence-type-50-90-di-pondok-cabe.html                           
    575     80   55       http://rumahdijual.com/depok/836518-rumah-manis-cluster-120-meter-dr-jalur-angkot-d.html                      
    575     78   60       http://rumahdijual.com/depok/965382-di-jual-rumah-di-beji-tanah-baru-depok.html                               
    575     78   60       http://rumahdijual.com/depok/965509-rumah-murah-di-beji-tanah-baru.html                                       
    575     78   60       http://rumahdijual.com/depok/914575-rumah-full-dak-townhouse-tanah-baru-depok.html                            
    575     78   60       http://rumahdijual.com/depok/969523-rumah-di-belakang-kampus-ui-depok.html                                    
    575     77   60       http://rumahdijual.com/depok/648208-rumah-memukau-harga-terjangkau-damai-residence.html                       
    575     75   50       http://rumahdijual.com/depok/750931-rumah-manis-minimalis-bisa-kpr-murah-cluster-tanah-baru.html              
    575     74   45       http://rumahdijual.com/depok/1278237-rumah-baru-inden-3-bulan-di-tanah-baru-3-a.html                          
    575     72   55       http://rumahdijual.com/depok/743983-rumah-baru-minimalis-bisa-kpr-dp-15-perumahan-villa.html                  
    575     72   55       http://rumahdijual.com/depok/664090-rumah-manis-minimalis-siap-huni-dan-kpr-di-perum.html                     
    575     72   55       http://rumahdijual.com/depok/751006-rumah-manis-minimalis-komplek-perum-villa-mutiara-cinere-siap.html        
    575     70   60       http://rumahdijual.com/depok/1295905-rumah-minimalis-berlokasi-strategis.html                                 
    575     70   50       http://rumahdijual.com/depok/1279413-rumah-murah-beji-kukusan-dekat-stasuin-paling-murah.html                 
    575     70   50       http://rumahdijual.com/depok/1279398-rumah-baru-di-kukusan-beji-depok-sisa-1-unit.html                        
    575     70   50       http://rumahdijual.com/depok/1099401-rumah-murah-depok.html                                                   
    575     70   50       http://rumahdijual.com/depok/1294393-paling-murah-rumah-dekat-stasiun-di-kukusan-beji-depok.html              
    575     69   50       http://rumahdijual.com/depok/1212488-rumah-nyaman-dalam-cluster-tenag-di-jalan-rtm-kelapa.html                
    578     91   45       http://rumahdijual.com/depok/1236849-rumah-cantik-dekat-gdc-depok-promo-cuma-dp-10-a.html                     
    578     91   45       http://rumahdijual.com/depok/1024956-rumah-cantik-dekat-gdc-depok-promo-cuma-dp-10-a.html                     
    578     72   40       http://rumahdijual.com/depok/1047184-cluster-murah-di-depok-pancoran-mas-daerah-margonda.html                 
    580     96   36       http://rumahdijual.com/depok/1172419-rumah-murah-dijual-di-gdc-depok-bisa-kpr.html                            
    580     96   36       http://rumahdijual.com/depok/1173412-rumah-baru-di-kawasan-depok.html                                         
    580     96   36       http://rumahdijual.com/depok/1272051-cluster-di-grand-depok-city-ada-kolam-renang-masjid.html                 
    580     96   36       http://rumahdijual.com/depok/1252316-lokasi-dekat-stasiun-depok-margonda-tol-cijago-dp-10-a.html              
    580     92   60       http://rumahdijual.com/depok/350005-robina-village-ready-stock.html                                           
    580     90   58       http://rumahdijual.com/depok/784895-dijual-rumah-baru-depok-rangkapan-jaya.html                               
    580     84   60       http://rumahdijual.com/depok/942108-rumah-cantik-di-kawasan-gdc.html                                          
    580     84   47       http://rumahdijual.com/depok/1171274-dijual-rumah-baru-lokasi-di-tanah-baru-depok.html                        
    580     82   60       http://rumahdijual.com/depok/1142810-rumah-dijual-di-griya-cinere.html                                        
    580     82   55       http://rumahdijual.com/depok/1041094-rumah-di-depok-2-r21-0331-a.html                                         
    580     81   50       http://rumahdijual.com/depok/1268724-rumah-bagus-murah-dekat-gdc-depok.html                                   
    580     78   48       http://rumahdijual.com/depok/1155375-rumah-cluster-kpr-di-tanah-baru-depok.html                               
    582     88   45       http://rumahdijual.com/depok/1300760-rumah-cantik-minimalis-di-tanah-baru-beji-dekat-per4an.html              
    584     92   60       http://rumahdijual.com/depok/991206-cluster-hanem-residence.html                                              
    585     91   36       http://rumahdijual.com/depok/1121736-rumah-baru-tipe-36-91-kpr-585jt-jl-raya.html                             
    585     90   60       http://rumahdijual.com/depok/1235556-dijual-rumah-lokasi-strategis-di-kalimulya-depok.html                    
    585     90   60       http://rumahdijual.com/depok/1222931-jual-rumah-ready-stock-kalimulya-depok.html                              
    585     90   50       http://rumahdijual.com/depok/1102087-rumah-baru-dp-suka-suka-sawangan-depok.html                              
    585     90   50       http://rumahdijual.com/depok/497545-rumah-baru-lokasi-dekat-pintu-tol.html                                    
    585     90   50       http://rumahdijual.com/depok/1104552-rumah-mewah-dp-50-jt-lokasi-strategis.html                               
    585     85   60       http://rumahdijual.com/depok/791857-green-lite-town-house-depok-hunian-baru-harga-miring.html                 
    585     84   47       http://rumahdijual.com/depok/696114-rumah-lingkungan-asri.html                                                
    585     84   47       http://rumahdijual.com/depok/882872-rumah-konsep-cluster-pusat-kota-depok-dp-minim-banyak.html                
    585     81   60       http://rumahdijual.com/depok/1151736-rumah-minimalis-beji-depok.html                                          
    585     80   60       http://rumahdijual.com/depok/888261-rumah-sawangan-menjadi-incaran-para-pencari-rumah-murah.html              
    585     80   60       http://rumahdijual.com/depok/805647-town-house-green-lite-di-depok.html                                       
    585     80   60       http://rumahdijual.com/depok/888733-greenlite-town-house-rumah-murah-sawangan-nilai-investasi-tinggi.html     
    585     80   60       http://rumahdijual.com/depok/805575-town-house-murah-di-sawangan-depok.html                                   
    585     80   60       http://rumahdijual.com/depok/797116-town-house-cantik-strategis-di-kota-depok.html                            
    585     80   60       http://rumahdijual.com/depok/889833-greenlite-town-house-rumah-murah-sawangan-nilai-investasi-tinggi.html     
    585     78   48       http://rumahdijual.com/depok/865823-new-greenputra-mandiri-48-72-tanah-baru-beji-depok.html                   
    585     78   48       http://rumahdijual.com/depok/1202335-rumah-green-putra-mandiri.html                                           
    585     78   45       http://rumahdijual.com/depok/882809-rumah-dp-super-ringan-di-pusat-kota-depok-banjir.html                     
    585     78   45       http://rumahdijual.com/depok/739267-lavinia-residence-hunian-asri-dan-sehat-dkt-exit-tol.html                 
    585     78   45       http://rumahdijual.com/depok/712160-cluster-hunian-sehat-dan-asri-lavinia-residence.html                      
    585     78   45       http://rumahdijual.com/depok/786236-cluster-minimalis-modern-lokasi-strategis.html                            
    585     78   45       http://rumahdijual.com/depok/900385-cluster-lavinia-residence-mampang-free-biaya-surat-surat-bphtb.html       
    585     78   45       http://rumahdijual.com/depok/762439-cluster-modren-design-cantik-lokasi-mantap.html                           
    585     78   45       http://rumahdijual.com/depok/933623-rumah-cantik-di-depok-dekat-mall-dp-ringgan-di.html                       
    585     78   45       http://rumahdijual.com/depok/953379-investasi-cerdas-di-rangkapan-jaya-dp-disesuaikan.html                    
    585     78   45       http://rumahdijual.com/depok/953231-hunian-dilokasi-strategis-dp-ringan.html                                  
    585     78   45       http://rumahdijual.com/depok/756423-cluster-cantik-dp-ringgan-di-cicil-free-legalitas.html                    
    585     78   45       http://rumahdijual.com/depok/753574-cluster-menarik-design-cantik-dp-ringgan.html                             
    585     78   45       http://rumahdijual.com/depok/933571-cluster-cantik-di-depok-lokasi-strategis-dp-ringgan-di.html               
    585     78   45       http://rumahdijual.com/depok/880166-lavinia-residence-cluster-modren-dp-ringgan-di-cicil.html                 
    585     78   45       http://rumahdijual.com/depok/814725-cluster-cantik-harga-terjangkau-dp-ringgan-di-cicil-free.html             
    585     78   45       http://rumahdijual.com/depok/1269780-lavinia-residence-lokasi-asik-spek-terbaik.html                          
    587     80   43       http://rumahdijual.com/depok/1218792-rumah-mewah-di-kawasan-sejuk-madrid-residence.html                       
    590     90   50       http://rumahdijual.com/depok/1118626-ready-stock-sisa-1-unnit.html                                            
    590     84   50       http://rumahdijual.com/depok/1268053-di-jual-rumah-minimalis-siap-huni-lokasi-strategis-nempel.html           
    590     75   60       http://rumahdijual.com/depok/1135666-rumah-murah-strategis-di-kukusan-beji-15-menit-ko.html                   
    593     78   40       http://rumahdijual.com/depok/362242-rumah-minimalis-type-40-perumahan-murah-di-depok-bisa.html                
    593     72   45       http://rumahdijual.com/depok/668093-green-ambara-gardenia-krukut-limo-cinere-depok.html                       
    594     78   55       http://rumahdijual.com/depok/822168-rumah-cantik-cluster-120-m-dr-jalur-angkot-d.html                         
    595     95   60       http://rumahdijual.com/depok/746180-perumahan-strategis-dicibinong-tdp-32-5jt-all-shm.html                    
    595     95   60       http://rumahdijual.com/depok/1035862-rumah-baru-1-lantai-aman-sejuk-dan-nyaman-di.html                        
    595     90   54       http://rumahdijual.com/depok/1253624-rumah-cimanggis.html                                                     
    595     90   54       http://rumahdijual.com/depok/1297993-rumah-siap-huni-di-radar-auri-depok.html                                 
    595     90   54       http://rumahdijual.com/depok/1309643-rumah-pijar-nirwan-cimanggis-depok.html                                  
    595     90   54       http://rumahdijual.com/depok/1297970-rumah-minimalis-dijual-di-radar-auri-cimanggis-depok.html                
    595     90   40       http://rumahdijual.com/depok/1048897-perumahan-di-kota-depok-strategis-nilai-invest-jika-dijual.html          
    595     80   45       http://rumahdijual.com/depok/1237444-rumah-asri-dijalan-juanda-depok.html                                     
    595     80   45       http://rumahdijual.com/depok/1237434-rumah-asri-dijalan-juanda-depok.html                                     
    595     79   50       http://rumahdijual.com/depok/750923-rumah-manis-minimalis-cluster-tanah-baru-depok-bisa-kpr.html              
    595     78   55       http://rumahdijual.com/depok/822162-rumah-manis-cluster-120-m-dr-jalur-angkot-d.html                          
    595     78   54       http://rumahdijual.com/depok/675872-segera-miliki-sisa-3-unit-type-54-78-a.html                               
    595     78   48       http://rumahdijual.com/depok/271619-rumah-di-depok-murah-dekat-rumah-sakit-di-depok.html                      
    595     78   42       http://rumahdijual.com/depok/1145119-rumah-murah-minimalis-dua-lantai-di-cimanggis-depok.html                 
    595     78   42       http://rumahdijual.com/depok/1201120-hunian-manis-lokasi-strategis-di-cimanggis.html                          
    595     78   42       http://rumahdijual.com/depok/1201103-rumah-cluster-murah-minimalis-di-cimanggis-depok.html                    
    595     78   42       http://rumahdijual.com/depok/1233201-cluster-murah-lokasi-strategis-pinggir-jalan-raya-di-cimanggis.html      
    595     75   55       http://rumahdijual.com/depok/822161-rumah-cantik-cluster-tanah-baru-depok-120-m-dr.html                       
    595     72   55       http://rumahdijual.com/depok/1040952-di-jual-rumah-cantik-minimalis-siap-huni-di-depok.html                   
    595     72   48       http://rumahdijual.com/depok/1032227-rumah-strategis-di-depok.html                                            
    595     72   45       http://rumahdijual.com/depok/1220701-perumahan-muslim-griya-pesona-juanda-depok.html                          
    595     72   36       http://rumahdijual.com/depok/764499-cluster-modern-nan-asri-di-lokasi-strategis-tanah-baru.html               
    595     72   36       http://rumahdijual.com/depok/764399-rumah-cluster-asri-siap-huni-di-raden-sanim-tanah.html                    
    595     71   41       http://rumahdijual.com/depok/1205074-rumah-di-tanah-baru.html                                                 
    595     71   41       http://rumahdijual.com/depok/1177097-rumah-modern-minimalis-di-tanah-baru-beji-dekat-ui.html                  
    596     90   30       http://rumahdijual.com/depok/982016-permata-cimanggis-depok.html                                              
    596     90   30       http://rumahdijual.com/depok/1189931-perumahan-murah-di-cimanggis-depok.html                                  
    596     90   30       http://rumahdijual.com/depok/624728-rumah-murah-di-depok-permata-cimanggis-001-a.html                         
    596     90   30       http://rumahdijual.com/depok/682708-rumah-di-depok-30-90-permata-cimanggis.html                               
    596     90   30       http://rumahdijual.com/depok/682707-rumah-di-depok-30-90-permata-cimanggis.html                               
    597     78   49       http://rumahdijual.com/depok/809863-rumah-cluster-1km-dari-tugu-tanah-baru-depok-harga.html                   
    598     84   45       http://rumahdijual.com/depok/1081101-rumah-idaman-pelangi-di-limo-grogol.html                                 
    598     84   45       http://rumahdijual.com/depok/1076200-rumah-cinere-town-house-pelangi-residence.html                           
    598     78   49       http://rumahdijual.com/depok/810766-rumah-baru-minimalis-di-tanah-baru-depok-bisa-kpr.html                    
    599     90   60       http://rumahdijual.com/depok/1146114-rumah-modern-depok-villa-pertiwi-shm-3km-dari-tol.html                   
    599     78   48       http://rumahdijual.com/depok/799804-perumahan-bisa-kpr-masuk-mobil-dekat-stasiun-ui.html                      
    599     78   48       http://rumahdijual.com/depok/357919-sisa-1-unit-ready-stock-perumahan-green-value-rumah.html                  
    599     78   42       http://rumahdijual.com/depok/812118-perumahan-di-tanah-baru-depok-dp-rendah-cicilan-ringan.html               
    600     97   38       http://rumahdijual.com/depok/1216226-over-kredit-rumah-di-lingkungan-aman-dan-asri.html                       
    600     97   38       http://rumahdijual.com/depok/1273320-dijual-rumah-over-kredit-di-bojong-sari-depok.html                       
    600     97   38       http://rumahdijual.com/depok/1249728-rumah-dijual-over-kredit-di-bojongsari-depok.html                        
    600     97   37       http://rumahdijual.com/depok/1031178-jual-rumah-hook-lokasi-strategis-lt-lb-97-37-a.html                      
    600     96   50       http://rumahdijual.com/depok/1169210-rumah-luas-siap-huni-di-grand-volue-depok.html                           
    600     94   55       http://rumahdijual.com/depok/725547-cluster-gandul-12-unit.html                                               
    600     92   60       http://rumahdijual.com/depok/1063961-rumah-murah-robina-village-sawangan.html                                 
    600     92   55       http://rumahdijual.com/depok/1015294-rumah-murah-di-kavling-ui-depok.html                                     
    600     92   55       http://rumahdijual.com/depok/1242190-rumah-type-55-92-tingkat-2-di-perumahan-puri.html                        
    600     92   54       http://rumahdijual.com/depok/1059844-dijual-murah-rumah-cluster-di-telaga-golf-sawangan-depok.html            
    600     92   54       http://rumahdijual.com/depok/1060332-rumah-cluster-dijual-di-sawangan-depok-ciputat.html                      
    600     92   54       http://rumahdijual.com/depok/1064909-dijual-rumah-di-depok.html                                               
    600     90   50       http://rumahdijual.com/depok/1088777-di-jual-rumah-minimalis-sipa-huni-nempel-grand-depok.html                
    600     90   50       http://rumahdijual.com/depok/983031-hunian-ready-stock-eksklusif-di-pinggir-jalan-sawangan.html               
    600     90   50       http://rumahdijual.com/depok/1021536-rumah-di-perumahan-griya-depok-asri.html                                 
    600     90   50       http://rumahdijual.com/depok/1011863-hunian-cluster-one-gate-1-2lantai-pinggir-jalan-ready.html               
    600     90   50       http://rumahdijual.com/depok/849776-rumah-siap-huni-di-komplek-bdn-sawangan-depok.html                        
    600     90   45       http://rumahdijual.com/depok/1042991-cluster-acacia-di-grand-depok-city.html                                  
    600     90   45       http://rumahdijual.com/depok/1060681-sawangan-residences-miliki-rumah-siap-huni.html                          
    600     90   45       http://rumahdijual.com/depok/1075109-cluster-acacia.html                                                      
    600     90   45       http://rumahdijual.com/depok/828725-rumah-dijual-rumah-samping-dengan-tol-jor-cimanggis-depok.html            
    600     90   45       http://rumahdijual.com/depok/1121775-rumah-di-kota-kembang-depok.html                                         
    600     90   38       http://rumahdijual.com/depok/1059536-rumah-murah-di-gdc.html                                                  
    600     90   38       http://rumahdijual.com/depok/1059534-rumah-dijual-murah-di-gdc-depok.html                                     
    600     90   38       http://rumahdijual.com/depok/1072974-jual-rumah-di-grand-depok-city.html                                      
    600     90   38       http://rumahdijual.com/depok/1057900-dijual-rumah-asri-di-depok.html                                          
    600     90   38       http://rumahdijual.com/depok/1098254-dijual-rumah-di-grand-depok-city.html                                    
    600     90   38       http://rumahdijual.com/depok/1057615-rumah-murah-dan-asri-di-grand-depok-city.html                            
    600     90   38       http://rumahdijual.com/depok/1091757-dijual-rumah-di-grand-depok-city-murah-hanya-600-a.html                  
    600     90   38       http://rumahdijual.com/depok/1059535-rumah-murah-di-grand-depok-city.html                                     
    600     90   38       http://rumahdijual.com/depok/1089429-rumah-dijual-di-depok.html                                               
    600     90   38       http://rumahdijual.com/depok/1092909-rumah-dijual-didepok.html                                                
    600     89   50       http://rumahdijual.com/depok/1231650-rumah-asri-di-pancoranmas-depok.html                                     
    600     88   55       http://rumahdijual.com/depok/1250832-jual-rumah-di-jatimulya-depok.html                                       
    600     87   50       http://rumahdijual.com/depok/1076604-rumah-cantik-harga-menarik.html                                          
    600     87   50       http://rumahdijual.com/depok/1077832-rumah-elit-harga-irit.html                                               
    600     84   56       http://rumahdijual.com/depok/1255352-rumah-dijual-di-mampang-indah-2-depok.html                               
    600     84   55       http://rumahdijual.com/depok/832142-rumah-manis-siap-bangun-cluster-kukusan-dkt-pintu-tol.html                
    600     84   53       http://rumahdijual.com/depok/748908-rumah-cantik-di-jalan-utama-di-sawangan.html                              
    600     84   48       http://rumahdijual.com/depok/1301230-30-di-jual-rumah-cluster-bangunan-baru-raden-saleh.html                  
    600     84   47       http://rumahdijual.com/depok/889576-rumah-cantik-sawangan-depok.html                                          
    600     84   45       http://rumahdijual.com/depok/589017-rumah-elit-harga-irit-gratis-biaya.html                                   
    600     84   38       http://rumahdijual.com/depok/1011530-rumah-murah-asri-permata-cimanggis-free-biaya.html                       
    600     84   36       http://rumahdijual.com/depok/1310889-rumah-strategis-full-furnished-dijual-murah-di-pondok-rajec.html         
    600     84   36       http://rumahdijual.com/depok/1310982-dijual-cepat-murah-rumah-di-pondok-rajeg-depok.html                      
    600     84   36       http://rumahdijual.com/depok/1311028-jual-cepat-rumah-600juta-di-depok-bu.html                                
    600     84   36       http://rumahdijual.com/depok/1301563-dijual-rumah-pribadi-pondok-rajek.html                                   
    600     83   53       http://rumahdijual.com/depok/721057-di-jual-rumah.html                                                        
    600     81   50       http://rumahdijual.com/depok/1063330-kavling-bakti-indah-pekapuran-sukamaju-baru-depok-r21-0352-a.html        
    600     81   45       http://rumahdijual.com/depok/1301155-rumah-di-cendana-regency-berada-di-area-jl-raya.html                     
    600     80   60       http://rumahdijual.com/depok/1248662-town-house-modern-minimalis-di-mampang-depok-siap-huni.html              
    600     80   55       http://rumahdijual.com/depok/1037502-rumah-strategis-di-beji-dekat-ui-dan-margonda.html                       
    600     79   50       http://rumahdijual.com/depok/1158404-rumah-hook-manis-cluster-120-m-dr-angkot-d.html                          
    600     79   47       http://rumahdijual.com/depok/703669-rumah-minimalis-asri-dan-nyaman-di-tanah-baru-depok.html                  
    600     78   42       http://rumahdijual.com/depok/790385-dekat-raden-sanim-tanah-baru-bisa-kpr.html                                
    600     78   36       http://rumahdijual.com/depok/1060160-perumahan-bukit-golf-cimanggis.html                                      
    600     75   54       http://rumahdijual.com/depok/1082241-rumah-di-jual.html                                                       
    600     74   43       http://rumahdijual.com/depok/902737-dijual-rumah-dalam-perumahan-permata-regency-depok-harga-600-a.html       
    600     73   42       http://rumahdijual.com/depok/1110116-vinewood-residence-hunian-modern-minimalis-di-tanah-baru-depok.html      
    600     72   55       http://rumahdijual.com/depok/877363-dijual-rumah-di-kelapa-2-depok-dkt-tol.html                               
    600     72   54       http://rumahdijual.com/depok/1094824-rumah-second-di-lokasi-terbaik-di-kota-depok.html                        
    600     72   50       http://rumahdijual.com/depok/1049114-dijual-rumah-di-pal-kelapa-dua-depok-harga-600-a.html                    
    600     72   36       http://rumahdijual.com/depok/701177-sawangan-residence-ideal-perumahan-asri-di-sawangan-depok-md454.html      
    600     70   50       http://rumahdijual.com/depok/1113264-rumah-kukusan-beji-lokasi-strategis-paling-murah-dan-nyaman.html         
    600     70   50       http://rumahdijual.com/depok/1294344-cluster-cantik-lokasi-strategis-di-beji-depok-jae.html                   
    600     70   50       http://rumahdijual.com/depok/1099501-cluster-cantik-dan-strategis-di-beji-depok.html                          
    600     70   50       http://rumahdijual.com/depok/1121363-cluster-strategis-akses-mudah-di-beji-depok.html                         
    600     70   50       http://rumahdijual.com/depok/1274587-perumahan-griya-lembah-depok-jawa-barat-rumah-aman-dan.html              
    600     70   50       http://rumahdijual.com/depok/1282550-rumah-bagus-harga-mempesona-di-derah-beji-depok.html                     
    600     70   50       http://rumahdijual.com/depok/1097587-rumah-minimalis-murah-di-jln-haji-asnawi-beji-depok.html                 
    600     70   50       http://rumahdijual.com/depok/1183102-rumah-beji-depok-lokasi-strategis-paling-murah-siap-huni.html            
    600     70   50       http://rumahdijual.com/depok/1135977-rumah-model-minimalis-dan-siap-huni-di-beji-kukusan.html                 
    600     70   50       http://rumahdijual.com/depok/1114675-rumah-beji-depok-lokasi-strategis-harga-manis-siap-huni.html             
    600     51   42       http://rumahdijual.com/depok/1185619-rumah-mewah-harga-bersaing-di-kawasan-kota-depok-kpr.html
    

## House Price Between 500 - 600 Mio IDR

### Visualize Data


```python
df = visualizeData('depok', 600, 700);
```


![png](png/output_59_0.png)


### Analyze the Data of House Price Between 600 - 700 Mio IDR


```python
avg = averageMeasures(df)
```

    
    AVERAGE MEASURES
    -----------------
    
    building    76
        land   106
       price   648
    


```python
mostSpacious(df)
```

    
    MOST SPACIOUS LAND
    -----------------
    
        bath     3
         bed     4
    building   400
        land   700
       price   685
         url   http://rumahdijual.com/depok/813095-rumah-besar-di-pasir-putih-sawangan.html
    
    MOST SPACIOUS BUILDING
    -----------------
    
        bath     1
         bed     2
    building   480
        land   102
       price   680
         url   http://rumahdijual.com/depok/931852-rumah-murah-sawangan-permai.html
    


```python
selectEconomical(df, avg, unit)
```

    
    MOST ECONOMICAL
    -----------------
    is when the price is really below average: 648 (million IDR) but you get above the average land: 106 (square meters) and above the average building: 76 (square meters)
    
    You are blessed to choose one of these 68  houses:
    
    price  land building                                                                                                      url
    600     400   120      http://rumahdijual.com/depok/1064129-rumah-tempat-tinggal-nyaman-dgn-tanah-luas-dan-lingkungan.html   
    600     270   100      http://rumahdijual.com/depok/1163246-rumah-baru-dijual-cepat-aman-dan-asri.html                       
    600     210   90       http://rumahdijual.com/depok/1107587-rumah-dijual-rumah-kampung-bertanah-luas-di-sawangan-depok.html  
    600     200   150      http://rumahdijual.com/depok/1050496-di-jual-rumah-kontrakan-4-pintu-dekat-jl-raya.html               
    600     200   100      http://rumahdijual.com/depok/1011067-rumah-lt-lb-200-100-di-rangkapan-jaya-depok.html                 
    600     159   90       http://rumahdijual.com/depok/1064794-dijual-rumah.html                                                
    600     150   80       http://rumahdijual.com/depok/1196688-cinangka-depok.html                                              
    600     150   200      http://rumahdijual.com/depok/1306307-rumah-2-lantai-masuk-mobil-di-kalimulya-300-meter.html           
    600     145   90       http://rumahdijual.com/depok/1126926-rumah-strategis-daerah-depok-murah.html                          
    600     135   141      http://rumahdijual.com/depok/979994-rumah-manis-di-putri-anggrek-mas-depok-jl-raya.html               
    600     134   134      http://rumahdijual.com/depok/1009121-dijual-murah-kontrakkan-4-pintu-lokasi-strategis.html            
    600     130   80       http://rumahdijual.com/depok/1016516-kavling-raden-saleh-hunian-megah-harga-menarik-hati.html         
    600     130   100      http://rumahdijual.com/depok/818514-luas-tanah-130-m2-depok-maharaja.html                             
    600     127   125      http://rumahdijual.com/depok/1166569-rumah-siap-huni-di-komplex-jatijajar-depok-jawa-barat.html       
    600     125   100      http://rumahdijual.com/depok/1173386-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html      
    600     121   80       http://rumahdijual.com/depok/915864-rumah-murah-di-beji-depok.html                                    
    600     121   100      http://rumahdijual.com/depok/1290717-dijual-rumah-cluster-murah-di-limo-cinere.html                   
    600     121   100      http://rumahdijual.com/depok/1091091-perumahan-murah-di-cimanggis-r21-0386-a.html                     
    600     120   160      http://rumahdijual.com/depok/878962-rumah-dijual-di-depok.html                                        
    600     120   100      http://rumahdijual.com/depok/1089946-rumah-cluster-jalan-pitara-raya-kota-depok.html                  
    600     120   100      http://rumahdijual.com/depok/1089704-cluster-modern-di-pitara-pancoran-mas-kota-depok.html            
    600     120   100      http://rumahdijual.com/depok/1098503-hunian-cluster-strategis-di-pitara-pancoran-mas-kota-depok.html  
    600     120   100      http://rumahdijual.com/depok/1098564-rumah-hunian-cluster-di-pitara-pancoran-mas-kota-depok.html      
    600     120   100      http://rumahdijual.com/depok/1089680-hunian-cluster-pemukiman-nyaman-dan-asri-pitara-pancoran-mas.html
    600     120   100      http://rumahdijual.com/depok/1120073-hunian-dalam-cluster-one-gate-system-di-pitara-depok.html        
    600     120   100      http://rumahdijual.com/depok/1133828-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html     
    600     120   100      http://rumahdijual.com/depok/1133855-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html     
    600     120   100      http://rumahdijual.com/depok/1109359-rumah-cluster-pancoran-mas-rangkapan-jaya-depok.html             
    600     120   100      http://rumahdijual.com/depok/1102750-perumahan-griya-pratama-asri-pancoran-mas-depok.html             
    600     120   100      http://rumahdijual.com/depok/1148317-perumahan-cluster-griya-pratama-asri-di-jalan-pitara-kota.html   
    600     120   100      http://rumahdijual.com/depok/1148322-one-gate-system.html                                             
    600     120   100      http://rumahdijual.com/depok/1148621-hunian-nyaman-dan-asri.html                                      
    600     120   100      http://rumahdijual.com/depok/1092057-rumah-cluster-pitara-kota-depok.html                             
    600     120   100      http://rumahdijual.com/depok/1092061-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html      
    600     120   100      http://rumahdijual.com/depok/1150673-rumah-cluster-jalan-pitara-pancoran-mas-depok.html               
    600     120   100      http://rumahdijual.com/depok/1150517-rumah-cluster-pitara-pancoran-mas-kota-depok.html                
    600     120   100      http://rumahdijual.com/depok/1148610-griya-pratama-asri.html                                          
    600     120   100      http://rumahdijual.com/depok/1133216-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html     
    600     120   100      http://rumahdijual.com/depok/1133203-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html     
    600     120   100      http://rumahdijual.com/depok/1138168-rumah-cluster-one-gate-system-pitara-pancoran-mas-depok.html     
    600     120   100      http://rumahdijual.com/depok/1133210-rumah-cluster-jalan-pitara-pancoran-mas-depok.html               
    600     120   100      http://rumahdijual.com/depok/1133027-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html     
    600     120   100      http://rumahdijual.com/depok/1132961-hunian-cluster-griya-pratama-asri-di-pitara-depok.html           
    600     120   100      http://rumahdijual.com/depok/1133352-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html     
    600     120   100      http://rumahdijual.com/depok/1133369-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html     
    600     120   100      http://rumahdijual.com/depok/1133414-rumah-cluster-pitara-pancoran-mas-kota-depok.html                
    600     120   100      http://rumahdijual.com/depok/1126678-rumah-cluster-one-gate-system.html                               
    600     120   100      http://rumahdijual.com/depok/1100006-hunian-dalam-cluster-di-pitara-pancoran-mas-depok.html           
    600     120   100      http://rumahdijual.com/depok/1131545-hunian-cluster-one-gate-system-di-jalan-pitara-pancoran.html     
    600     120   100      http://rumahdijual.com/depok/1138161-perumahan-cluster-griya-pratama-asri.html                        
    600     120   100      http://rumahdijual.com/depok/1173218-rumah-depok.html                                                 
    600     117   85       http://rumahdijual.com/depok/1158180-dijual-rumah-murah-di-serua-bojongsari-depok.html                
    600     115   200      http://rumahdijual.com/depok/836205-rumah-perumnas-gelatik-depok-1-a.html                             
    600     110   80       http://rumahdijual.com/depok/1070207-di-jual-rumah-minimalis-dalem-kompleks.html                      
    600     110   110      http://rumahdijual.com/depok/756919-rumah-di-h-zakaria-tanah-baru.html                                
    600     110   110      http://rumahdijual.com/depok/979163-dijual-cepat-rumah-daerah-depok.html                              
    600     110   100      http://rumahdijual.com/depok/1107993-rumah-luas-full-granit-di-pitara-depok.html                      
    600     110   100      http://rumahdijual.com/depok/1107996-hunian-hook-dekat-jalan-raya-di-pitara-pancoran-mas.html         
    620     144   140      http://rumahdijual.com/depok/684570-rumah-memukau-harga-terjangkau.html                               
    620     112   90       http://rumahdijual.com/depok/961957-dijual-rumah-di-depok-timur-bni.html                              
    625     122   100      http://rumahdijual.com/depok/935949-rumah-murah-di-hook-perumnas-depok-timur.html                     
    625     120   80       http://rumahdijual.com/depok/1133535-rumah-asri-dan-nyaman-di-villa-pamulang-depok.html               
    625     120   80       http://rumahdijual.com/depok/1133319-villa-pamulang-depok-stage-humble-attiude.html                   
    625     120   120      http://rumahdijual.com/depok/1068624-ruman-nyaman-dan-asri-di-perumahan-mekar-perdana-depok.html      
    625     120   120      http://rumahdijual.com/depok/740988-rumah-perumnas-depok-1-a.html                                     
    630     238   150      http://rumahdijual.com/depok/1095670-rumah-hunian-asri-sindangkarsa-depok.html                        
    630     208   150      http://rumahdijual.com/depok/1197672-di-jual-rumah-tanah-luas-harga-bersahabat-dalam-perumahan.html   
    645     120   80       http://rumahdijual.com/depok/1080296-rumah-dekat-parung-bingung-sawangan-kubah-emas.html
    


```python
selectModerate(df, avg, unit)
```

    
    MODERATE PRICE
    -----------------
    is when the price is above average: 648 (million IDR) with above-average land: 106 (square meters) and above-average building: 76 (square meters)
    
    
    There are : 252  items with above-average price and above-average land.
    
    There are : 171  items with above-average price, above-average land and above-average building.
    
    price  land building                                                                                                          url
    649     136   110      http://rumahdijual.com/depok/1301192-28-di-jual-rumah-bagus-ada-kios-depok-timur.html                     
    650     450   200      http://rumahdijual.com/depok/1208118-kontrakan-6-pintu-tanah-450m-masuk-mobil-nempel-sutet.html           
    650     430   200      http://rumahdijual.com/depok/1237768-jual-butuh-rumah-dan-tanah.html                                      
    650     350   150      http://rumahdijual.com/depok/681144-dijual-rumah-di-sawangan-depok.html                                   
    650     350   100      http://rumahdijual.com/depok/1228790-kontrakan-4-pintu-tanah-350-meter-di-jatijajar-depok.html            
    650     305   305      http://rumahdijual.com/depok/699295-rumah-sederhana.html                                                  
    650     250   200      http://rumahdijual.com/depok/1080770-dijual-rumah-di-sawangan-depok.html                                  
    650     250   150      http://rumahdijual.com/depok/1067680-di-jual-rumah-murah-tanah-luas-desain-mewah-fasilitas.html           
    650     214   90       http://rumahdijual.com/depok/95751-rumah-siap-huni-dan-murah.html                                         
    650     210   100      http://rumahdijual.com/depok/506507-jual-rumah-baru-luas-210m-di-jl-jati-indah.html                       
    650     203   94       http://rumahdijual.com/depok/923176-rumah-hanya-3-menit-ke-stasiun-kereta-untuk-hunian.html               
    650     203   94       http://rumahdijual.com/depok/1243661-depok-lama-rumah-3-menit-ke-stasiun-kereta-siap.html                 
    650     202   85       http://rumahdijual.com/depok/999696-di-jual-rumah-cantik-tanah-luas-di-kali-mulya.html                    
    650     200   180      http://rumahdijual.com/depok/917925-dijual-rumah-di-cimanggis-depok.html                                  
    650     191   150      http://rumahdijual.com/depok/903113-rumah-lt-191-lb-150-tingkat-3-kolam-renang.html                       
    650     178   110      http://rumahdijual.com/depok/1078460-rumah-dan-warung.html                                                
    650     170   120      http://rumahdijual.com/depok/1104438-rumah-strategis-dalam-kota-depok.html                                
    650     169   130      http://rumahdijual.com/depok/888811-rumah-cantik-siap-huni.html                                           
    650     158   200      http://rumahdijual.com/depok/952819-rumah-sejuk-asri-dan-tenang-depok.html                                
    650     152   150      http://rumahdijual.com/depok/1114895-rumah-dijual-murah-depok-ada-2-rumah-1-shm.html                      
    650     150   100      http://rumahdijual.com/depok/1268180-rumah-besar-siap-masuk-di-cimanggis-akses-2-pintu.html               
    650     150   100      http://rumahdijual.com/depok/1233977-rumah-baru-di-perumahan-sukatani-depok-mewah-hook.html               
    650     145   90       http://rumahdijual.com/depok/1144002-rumah-gaya-betawi-di-mampang-depok.html                              
    650     136   100      http://rumahdijual.com/depok/1056969-rumah-toko-depok-timur.html                                          
    650     135   145      http://rumahdijual.com/depok/304632-rumah-baru-2-lantai.html                                              
    650     130   120      http://rumahdijual.com/depok/1235380-ready-siap-huni-rumah-2-lantai.html                                  
    650     130   100      http://rumahdijual.com/depok/1131590-griya-pratama-asri-pancoran-mas-depok.html                           
    650     130   100      http://rumahdijual.com/depok/889974-jual-rmh-murahhhh-di-maharaja-depok-650jt.html                        
    650     130   100      http://rumahdijual.com/depok/1189483-rumah-2-lantai-harga-murah-sekota-depok.html                         
    650     125   90       http://rumahdijual.com/depok/1300828-rumah-asri-siap-huni-di-depok.html                                   
    650     125   100      http://rumahdijual.com/depok/1177534-rumah-minimalis-kota-depok.html                                      
    650     125   100      http://rumahdijual.com/depok/1177353-rumah-cluster-kota-depok.html                                        
    650     125   100      http://rumahdijual.com/depok/1191608-cluster-pitra-dekat-jalan-raya-pitara-depok.html                     
    650     125   100      http://rumahdijual.com/depok/1175006-rumah-cluster-modern-kota-depok.html                                 
    650     125   100      http://rumahdijual.com/depok/1177782-rumah-cluster-100-125-pitaradepok.html                               
    650     125   100      http://rumahdijual.com/depok/1209416-griya-pratama-asri-pitara-depok.html                                 
    650     125   100      http://rumahdijual.com/depok/1209401-rumah-cluster-di-pitara-kota-depok-lantai-full-granite.html          
    650     125   100      http://rumahdijual.com/depok/1062727-rumah-cluster-pancoran-mas-depok.html                                
    650     125   100      http://rumahdijual.com/depok/1058833-cluster-3-kamar-tidur-shm.html                                       
    650     125   100      http://rumahdijual.com/depok/1195852-hunian-cluster-di-pitara-kota-depok-lantai-full-granite.html         
    650     125   100      http://rumahdijual.com/depok/1195836-griya-pratama-asri-siap-huni.html                                    
    650     125   100      http://rumahdijual.com/depok/1195827-unit-terbatas-rumah-luas.html                                        
    650     125   100      http://rumahdijual.com/depok/1195800-griya-pratama-asri-siap-huni.html                                    
    650     125   100      http://rumahdijual.com/depok/1195793-rumah-cluster-pitara-pancoran-mas-kota-depok.html                    
    650     125   100      http://rumahdijual.com/depok/1195787-griya-pratama-asri-siap-huni.html                                    
    650     125   100      http://rumahdijual.com/depok/1195821-rumah-cluster-pitara-kota-depok.html                                 
    650     125   100      http://rumahdijual.com/depok/1174997-rumah-cluster-pitara-depok.html                                      
    650     125   100      http://rumahdijual.com/depok/1168015-rumah-3-kamar.html                                                   
    650     125   100      http://rumahdijual.com/depok/1167995-rumah-bervariasi-tipe-pitara-depok.html                              
    650     125   100      http://rumahdijual.com/depok/1183396-griya-pratama-asri-siap-huni.html                                    
    650     123   123      http://rumahdijual.com/depok/649289-jual-rumah-di-depok-1-belakang-stadion-bola.html                      
    650     121   90       http://rumahdijual.com/depok/1009323-rumah-dijual-di-depok.html                                           
    650     121   90       http://rumahdijual.com/depok/982727-rumah-dijual-di-cibinong-depok-baru.html                              
    650     121   90       http://rumahdijual.com/depok/1075117-rumah-murah-siap-huni-di-cibinong-bojong-depok-baru.html             
    650     120   90       http://rumahdijual.com/depok/1092386-rumah-daerah-depok.html                                              
    650     120   90       http://rumahdijual.com/depok/1272249-185-di-jual-rumah-bagus-perumnas-ir-h-juanda.html                    
    650     120   80       http://rumahdijual.com/depok/1039321-rumah-besar-harga-kecil.html                                         
    650     120   120      http://rumahdijual.com/depok/795082-rumah-perumnas-depok-2-a.html                                         
    650     120   100      http://rumahdijual.com/depok/1230812-di-jual-rumah-cluster.html                                           
    650     120   100      http://rumahdijual.com/depok/805570-jual-rumah-perumnas-murah-depok.html                                  
    650     120   100      http://rumahdijual.com/depok/1107173-rumah-di-pitara-depok-full-granite-new-arrival.html                  
    650     120   100      http://rumahdijual.com/depok/1050738-rumah-keluarga-nyaman-untuk-semua.html                               
    650     120   100      http://rumahdijual.com/depok/1107839-rumah-cluster-tanah-luas-bangunan-besar-dipitara-depok.html          
    650     120   100      http://rumahdijual.com/depok/1122301-rumah-ready-stock-di-pitara-depok.html                               
    650     118   90       http://rumahdijual.com/depok/990971-rumah-di-kalimulya-hunian-megah-dan-cantik.html                       
    650     115   200      http://rumahdijual.com/depok/950331-dijual-rumah-di-pancoran-emas-depok-shm-2-lantai.html                 
    650     113   180      http://rumahdijual.com/depok/1266653-rumah-bu-bangunsn-60-dlm-tahap-finishing-di-jln.html                 
    650     112   120      http://rumahdijual.com/depok/1044125-rumah-bagus-lt112-lb120-650-jt-di-bukit-golf.html                    
    650     108   93       http://rumahdijual.com/depok/973057-dijual-rumah-di-tole-iskandar-depok.html                              
    650     108   125      http://rumahdijual.com/depok/1117084-di-jual-rumah-rumah-type-modern-di-sawangan-depok.html               
    650     107   90       http://rumahdijual.com/depok/1312156-rumah-di-daerah-strategis-dengan-cicilan-terjangkau-fixed-selama.html
    650     107   90       http://rumahdijual.com/depok/1311637-rumah-di-daerah-strategis-dengan-cicilan-terjangkau-fixed-selama.html
    650     107   90       http://rumahdijual.com/depok/1311376-rumah-di-daerah-strategis-dengan-cicilan-terjangkau-fixed-selama.html
    650     107   90       http://rumahdijual.com/depok/1311036-rumah-di-daerah-strategis-dengan-cicilan-terjangkau-fixed-selama.html
    650     107   90       http://rumahdijual.com/depok/1310865-rumah-di-mampang-pancoran-mas-depok.html                             
    650     107   90       http://rumahdijual.com/depok/1312480-rumah-di-daerah-strategis-dengan-cicilan-terjangkau-fixed-selama.html
    650     107   90       http://rumahdijual.com/depok/1315356-rumah-dengan-harga-ringan-di-kawasan-strategis-pancoran-mas.html     
    650     107   90       http://rumahdijual.com/depok/1270038-rumah-siap-huni-3-kamar-di-villa-pancoran-mas.html                   
    650     107   90       http://rumahdijual.com/depok/1314779-rumah-dengan-harga-ringan-di-kawasan-strategis-pancoran-mas.html     
    650     107   90       http://rumahdijual.com/depok/1246503-rumah-siap-huni-3-kamar-di-villa-pancoran-mas.html                   
    650     107   90       http://rumahdijual.com/depok/1314317-rumah-dengan-harga-ringan-di-kawasan-strategis-pancoran-mas.html     
    650     107   90       http://rumahdijual.com/depok/1314034-rumah-dengan-harga-ringan-di-kawasan-strategis-pancoran-mas.html     
    650     107   90       http://rumahdijual.com/depok/1260307-rumah-600-jutaan-di-pancoran-mas-depok-akses-strategis.html          
    650     107   90       http://rumahdijual.com/depok/1259813-rumah-di-mampang-pancoran-mas-depok.html                             
    650     107   90       http://rumahdijual.com/depok/1275309-rumah-600-jutaan-di-pancoran-mas-depok-akses-strategis.html          
    650     107   90       http://rumahdijual.com/depok/1274917-rumah-di-daerah-strategis-dengan-cicilan-terjangkau-fixed-selama.html
    650     107   90       http://rumahdijual.com/depok/1258157-rumah-di-mampang-pancoran-mas-depok.html                             
    650     107   90       http://rumahdijual.com/depok/1253863-rumah-600-jutaan-di-pancoran-mas-depok-akses-strategis.html          
    650     107   90       http://rumahdijual.com/depok/1254475-rumah-di-mampang-pancoran-mas-depok.html                             
    650     107   90       http://rumahdijual.com/depok/1307185-rumah-di-mampang-pancoran-mas-depok.html                             
    650     107   90       http://rumahdijual.com/depok/1296691-rumah-600-jutaan-di-pancoran-mas-depok-akses-strategis.html          
    650     106   113      http://rumahdijual.com/depok/740704-rumah-second-bermutu.html                                             
    654     157   187      http://rumahdijual.com/depok/1081900-rumah-2-pintu-2-lt-2-kwh-2-mbl.html                                  
    660     119   80       http://rumahdijual.com/depok/854054-rumah-luas-strategis-di-griya-kharisma-cilodong-depok.html            
    660     114   86       http://rumahdijual.com/depok/938479-rumah-siap-huni-di-depok.html                                         
    675     280   200      http://rumahdijual.com/depok/1151424-hunian-luas-dan-asri-daerah-sukmajaya.html                           
    675     234   90       http://rumahdijual.com/depok/927742-rumah-griya-telaga-permai-cimanggis.html                              
    675     200   185      http://rumahdijual.com/depok/1019320-di-jual-rumah-asri-suasana-alam-di-depok-lama.html                   
    675     128   80       http://rumahdijual.com/depok/929260-rumah-depok-tanah-bangunan-luas.html                                  
    675     125   250      http://rumahdijual.com/depok/997354-rumah-tingkat-dijual-murah-karena-butuh-uang-bangunan-kokoh.html      
    675     124   80       http://rumahdijual.com/depok/635190-rumah-minimalis-dekat-grand-depok-city.html                           
    675     120   95       http://rumahdijual.com/depok/1246528-rumah-hook-siap-huni-3-kamar-di-pancoran-mas.html                    
    675     120   95       http://rumahdijual.com/depok/1262834-rumah-hook-siap-huni-3-kamar-di-villa-pancoran.html                  
    675     120   95       http://rumahdijual.com/depok/1309600-rumah-hook-siap-huni-3-kamar-di-villa-pancoran.html                  
    675     120   90       http://rumahdijual.com/depok/1256166-info-rumah-dijual-murah-di-depok-dijual-rumah-di.html                
    678     200   185      http://rumahdijual.com/depok/1001997-di-jual-rumah-minimalis-di-kampung-sawah-depok.html                  
    680     154   120      http://rumahdijual.com/depok/1260439-rumah-luas-nyaman-di-taman-duta-cisalak-depok.html                   
    680     154   120      http://rumahdijual.com/depok/1245303-rumah-luas-nyaman-di-taman-duta-cisalak-depok.html                   
    680     154   120      http://rumahdijual.com/depok/1254299-rumah-luas-nyaman-di-taman-duta-cisalak-depok.html                   
    680     154   120      http://rumahdijual.com/depok/1242723-rumah-luas-nyaman-di-taman-duta-cisalak-depok.html                   
    680     120   108      http://rumahdijual.com/depok/917625-jual-rumah-di-wismamas-pondok-cabe.html                               
    685     700   400      http://rumahdijual.com/depok/813095-rumah-besar-di-pasir-putih-sawangan.html                              
    685     129   129      http://rumahdijual.com/depok/1299476-dijual-rumah-di-serua-bojong-sari-depok.html                         
    690     264   110      http://rumahdijual.com/depok/1300252-rumah-nyaman-di-reni-jaya-sawangan-depok.html                        
    695     400   120      http://rumahdijual.com/depok/1301162-25-di-jual-tanah-bangunan-banjaran-pucung-jatijajar-depok.html       
    695     155   100      http://rumahdijual.com/depok/1004971-dijual-rumah-di-cilodong-depok.html                                  
    695     155   100      http://rumahdijual.com/depok/1006327-rumah-siap-huni-di-perumahan-kalibaru-permai-cilodong-depok.html     
    695     136   90       http://rumahdijual.com/depok/899724-di-jual-rumah-bagus-perumnas-depok-timur-253-a.html                   
    695     108   80       http://rumahdijual.com/depok/532918-rumah-mungil-depok.html                                               
    695     108   108      http://rumahdijual.com/depok/945526-rumah-menarik-harga-cantik.html                                       
    699     108   80       http://rumahdijual.com/depok/1028983-rumah-di-grand-depok-city.html                                       
    700     335   100      http://rumahdijual.com/depok/223621-rumah-asri-dan-nyaman-di-cinangka-sawangan-depok.html                 
    700     288   150      http://rumahdijual.com/depok/1226545-rumah-luas-plus-kontrakan-2-pintu.html                               
    700     234   150      http://rumahdijual.com/depok/982832-dijual-rumah-dikalimulya-depok.html                                   
    700     230   230      http://rumahdijual.com/depok/1313340-jual-rumah-aman-dan-nyaman.html                                      
    700     225   225      http://rumahdijual.com/depok/1087454-rumah-megah-lt-225-lb-225-di-sidamukti-depok.html                    
    700     210   150      http://rumahdijual.com/depok/1039975-rumah-murah-lantai-full-granite-di-depok.html                        
    700     210   150      http://rumahdijual.com/depok/1037277-rumah-hunian-murah-luas-puas-strategis-di-depok.html                 
    700     207   150      http://rumahdijual.com/depok/1060483-rumah-luas-murah-dan-lantai-full-memakai-granit-di.html              
    700     200   200      http://rumahdijual.com/depok/1288199-dijual-rumah-di-depok-200m2-15-menit-dari-margonda.html              
    700     200   150      http://rumahdijual.com/depok/1159445-rumah-dijual.html                                                    
    700     200   120      http://rumahdijual.com/depok/1303803-di-jual-rumah-asri-siap-huni-tanah-luas-di.html                      
    700     200   100      http://rumahdijual.com/depok/1092066-rumah-dan-gudang-di-depok-pitara-200-m2.html                         
    700     185   85       http://rumahdijual.com/depok/796309-rumah-kalimulya-grand-depok-city-luas-185mtr.html                     
    700     180   170      http://rumahdijual.com/depok/817831-dijual-rumah-di-pinggir-jalan-cinangka-depok.html                     
    700     180   150      http://rumahdijual.com/depok/1078163-dijual-rumah-besar-dan-nyaman-di-perumahan-sukatani-permai.html      
    700     156   146      http://rumahdijual.com/depok/1252794-jual-cepat-saja-perumahan-kopassus-di-sukatani-harga-miring.html     
    700     155   100      http://rumahdijual.com/depok/1022033-rumah-di-kalibaru-cilodong-depok-sisw.html                           
    700     155   100      http://rumahdijual.com/depok/1001162-hunian-nyaman-dan-asri-harga-terjangkau-cilodong-depok.html          
    700     150   150      http://rumahdijual.com/depok/1130635-hunian-akses-mudah-jalan-kaki-ke-stasiun-citayam-dan.html            
    700     150   100      http://rumahdijual.com/depok/769277-rumah-indah-dan-bersih-di-sawangan-depok.html                         
    700     144   135      http://rumahdijual.com/depok/1233370-rumah-di-jln-tanah-baru-gg-swadaya1-no15.html                        
    700     140   120      http://rumahdijual.com/depok/1275244-rumah-cluster-5-kamar-tindu-jalan-2-mobil.html                       
    700     140   120      http://rumahdijual.com/depok/1214241-depok-mampang-sawangan-rumah-dengan-5-kamar-tidur.html               
    700     138   100      http://rumahdijual.com/depok/981143-rumah-baru-siap-huni-138-meter-area-gdc-depok.html                    
    700     138   100      http://rumahdijual.com/depok/1157586-rumah-second-siap-huni-baru-renov-di-kelapa-2-a.html                 
    700     135   80       http://rumahdijual.com/depok/1234402-rumah-minimalis-di-cilodong.html                                     
    700     135   125      http://rumahdijual.com/depok/778103-rumah-semi-minimalis-komplek-taman-duta-cisalak-depok.html            
    700     134   80       http://rumahdijual.com/depok/714145-di-jual-rumah-cantik-di-perumahan-depok-lama.html                     
    700     130   80       http://rumahdijual.com/depok/769831-rumah-cantik-pondok-rajeg-dekat-grand-depok-city.html                 
    700     130   100      http://rumahdijual.com/depok/325672-jual-rumah-depok.html                                                 
    700     130   100      http://rumahdijual.com/depok/1084143-dijual-rumah-minimalis-cantik-di-lokasi-strategis-dekat-kampus.html  
    700     125   89       http://rumahdijual.com/depok/901001-rumah-asri-depok.html                                                 
    700     125   110      http://rumahdijual.com/depok/283438-rumah-di-depok.html                                                   
    700     124   117      http://rumahdijual.com/depok/1241025-dijual-cepat-tamansari-puribali-sawangan-depok.html                  
    700     124   115      http://rumahdijual.com/depok/1056125-dijual-rumah-tamansari-puribali-sawangan-depok.html                  
    700     122   140      http://rumahdijual.com/depok/754570-rumah-bagus-di-bojongsari.html                                        
    700     120   90       http://rumahdijual.com/depok/946832-rumah-murah-bagus-dijual-sangat-cepat-di-depok.html                   
    700     120   120      http://rumahdijual.com/depok/669226-kavling-sasak-harga-pantas-unit-terbatas.html                         
    700     120   100      http://rumahdijual.com/depok/1236509-rumah-anyar-perum-bumi-panmas-depok.html                             
    700     120   100      http://rumahdijual.com/depok/1110575-rumah-di-citayam-depok.html                                          
    700     116   90       http://rumahdijual.com/depok/1059843-rumah-cantik-dan-minimalis-harga-terjangkau.html                     
    700     115   115      http://rumahdijual.com/depok/1158155-rumah-murah-strategis-di-depok.html                                  
    700     110   90       http://rumahdijual.com/depok/698730-kavling-pertanian-unit-terbatas-harga-pantas.html                     
    700     110   100      http://rumahdijual.com/depok/926851-rumah-second-2-lantai-di-perumahan-lembah-nirmala-cimanggis.html      
    700     108   80       http://rumahdijual.com/depok/930827-rumah-1-5-lantai-di-grand-depok-city.html                             
    700     108   80       http://rumahdijual.com/depok/1027376-rumah-siap-huni-di-kawasan-gdc-depok.html                            
    700     108   170      http://rumahdijual.com/depok/956851-di-jual-rumah-di-perumahan-mekarsari-cimanggis-289-a.html             
    700     108   100      http://rumahdijual.com/depok/932678-rumah-cluster-nempel-grand-depok-city.html                            
    700     107   90       http://rumahdijual.com/depok/1021437-rumah-asri-di-cimanggis.html                                         
    700     106   82       http://rumahdijual.com/depok/621408-jl-raya-kerukut-kecamatn-limo.html
    


```python
selectExpensive(df, avg, unit)
```

    
    EXPENSIVE PRICE
    -----------------
    is when the price is above average: 648 (million IDR) but you only get land below average: 106 (square meters) and building below average: 76 (square meters).
    
    
    
    There are : 255  items that matched the EXPENSIVE category.
    
    price  land building                                                                                                                   url
    648     90    45       http://rumahdijual.com/depok/1151789-rumah-cluster-siap-huni-di-sawangan-depok.html                                
    648     72    69       http://rumahdijual.com/depok/776562-rumah-dijual-dalam-cluster-mepet-calon-pintu-toll-cinere.html                  
    649     84    50       http://rumahdijual.com/depok/863286-rumah-new-full-furnished-murah-jl-raden-sanim-tanah.html                       
    649     72    38       http://rumahdijual.com/depok/960447-rumah-murah-tanpa-dp-siap-huni-di-cimanggis-depok.html                         
    649     72    38       http://rumahdijual.com/depok/964923-rumah-murah-dp-ringan-strategis-dan-bebas-banjir-di.html                       
    649     72    38       http://rumahdijual.com/depok/978701-rumah-dijual-di-cimanggis-depok.html                                           
    649     72    38       http://rumahdijual.com/depok/980860-rumah-cantik-tanpa-dp-hanya-5-menit-dari-exit.html                             
    650     98    75       http://rumahdijual.com/depok/1312528-rumah-murah-di-tanah-baru-depok.html                                          
    650     98    60       http://rumahdijual.com/depok/906205-perumahan-green-putra-mandiri-rumah-yang-siap-huni-dan.html                    
    650     98    60       http://rumahdijual.com/depok/1044263-rumah-murah-di-sawangan-ready-stock.html                                      
    650     97    45       http://rumahdijual.com/depok/1236188-cluster-alpinia-gdc.html                                                      
    650     95    75       http://rumahdijual.com/depok/894092-pojokan-murah-cluster-120-meter-dr-angkot-d-105-a.html                         
    650     95    60       http://rumahdijual.com/depok/1296813-rumah-murah-siap-huni-di-tanah-baru.html                                      
    650     93    65       http://rumahdijual.com/depok/1271784-rumah-cluster-siap-huni-di-tanah-baru.html                                    
    650     92    45       http://rumahdijual.com/depok/798351-rumah-cluster-eight-town-house.html                                            
    650     91    54       http://rumahdijual.com/depok/1029288-rumah-deket-samsat-cinere-rp-600jutaan.html                                   
    650     91    54       http://rumahdijual.com/depok/1052637-cinere-garden-court-hanya-650-juta.html                                       
    650     90    70       http://rumahdijual.com/depok/900595-perumnas-rumah-baru-depok-2-tengah-jalur-angkot-24-a.html                      
    650     90    70       http://rumahdijual.com/depok/1160450-rumah-murah-siap-huni-dan-kpr-cluster-5-menit.html                            
    650     90    70       http://rumahdijual.com/depok/1232934-rumah-siap-huni.html                                                          
    650     90    70       http://rumahdijual.com/depok/1280641-rumah-ready-di-depok-timur-r21-0470-a.html                                    
    650     90    60       http://rumahdijual.com/depok/1042648-dijual-rumah-murah-di-beji-depok.html                                         
    650     90    60       http://rumahdijual.com/depok/1266182-rumah-baru-minimalis-strategis-perumahan-besar-di-tanah-baru.html             
    650     90    54       http://rumahdijual.com/depok/1260218-rumah-minimalis-cimanggis.html                                                
    650     90    54       http://rumahdijual.com/depok/750592-rumah-indent-di-komplek-pendowo-limo-depok-type-54-a.html                      
    650     90    50       http://rumahdijual.com/depok/865822-dijual-cepat-rumah-di-felicity-townhouse-cinangka-sawangan-depok.html          
    650     88    70       http://rumahdijual.com/depok/1209411-rumah-di-depok-beji-luas-88-mtr.html                                          
    650     88    66       http://rumahdijual.com/depok/1161677-rumah-siap-huni-tanah-baru-depok.html                                         
    650     88    66       http://rumahdijual.com/depok/1001385-rumah-asri-aman-nyaman-di-tanah-baru-beji-depok.html                          
    650     88    66       http://rumahdijual.com/depok/1218509-di-tanah-baru-depok-ada-rumah-murah-bersertifikat.html                        
    650     88    66       http://rumahdijual.com/depok/1118503-rumah-cluster-second-di-tanah-baru-depok.html                                 
    650     88    66       http://rumahdijual.com/depok/1141675-rumah-second-di-tanah-baru-depok.html                                         
    650     88    66       http://rumahdijual.com/depok/1265884-rumah-siap-huni-tanah-baru-depok.html                                         
    650     88    60       http://rumahdijual.com/depok/1072570-cluster-perdamaian-ii-tanah-baru-depok.html                                   
    650     85    68       http://rumahdijual.com/depok/1281950-di-jual-perumahan-baru-minimalis-dalem-cluster.html                           
    650     85    68       http://rumahdijual.com/depok/1284474-di-jual-perumahan-baru-minimalis-dalem-cluster.html                           
    650     84    70       http://rumahdijual.com/depok/485227-rumah-2-lantai-rp-650jt-akses-jalan-lokasi-lebar.html                          
    650     84    65       http://rumahdijual.com/depok/1310842-hunian-nyaman-dalam-perumahan-mulya-asri-tanah-baru-depok.html                
    650     84    50       http://rumahdijual.com/depok/709412-di-jual-rumah-di-perumahan-belacassa-depok-59-a.html                           
    650     84    40       http://rumahdijual.com/depok/1258891-rumah-idaman-murah-nyaman-dan-asri-bisa-take-over.html                        
    650     84    40       http://rumahdijual.com/depok/1060053-rumah-minimalis-dan-cantik-de-casa-cibubur.html                               
    650     82    45       http://rumahdijual.com/depok/1249797-grand-pesona-depok.html                                                       
    650     80    72       http://rumahdijual.com/depok/1209874-rumah-2-lt-minimalist-lokasi-strategis-pinggir-jalan-raya.html                
    650     80    65       http://rumahdijual.com/depok/1270188-town-house-amethyst-residence-650jt-nego.html                                 
    650     80    60       http://rumahdijual.com/depok/1158411-rumah-cantik-cluster-120-m-dr-angkot-d-105-a.html                             
    650     80    54       http://rumahdijual.com/depok/978083-rumah-new-aruna-residences.html                                                
    650     80    40       http://rumahdijual.com/depok/863598-rumah-di-cimanggis-depok-dekat-pintu-tol-cisalak-puri.html                     
    650     80    36       http://rumahdijual.com/depok/1189441-rumah-masih-gress-di-pancoran-mas-depok.html                                  
    650     79    50       http://rumahdijual.com/depok/1074770-rumah-di-cibubur-sangat-strategis-nyaman-minimalis-dan-di.html                
    650     78    45       http://rumahdijual.com/depok/865907-jual-cepat-rmh-cahaya-residence-tanah-baru-pancoranmas-depok.html              
    650     76    45       http://rumahdijual.com/depok/1299363-19-di-jual-over-kredit-rumah-cantik-cluster-kalimulya.html                    
    650     76    40       http://rumahdijual.com/depok/1157022-rumah-dijual-cepat.html                                                       
    650     75    70       http://rumahdijual.com/depok/862253-rumah-cantik-harga-menarik-di-greel-village.html                               
    650     73    45       http://rumahdijual.com/depok/1048881-dijual-rumah-3-unit-di-mekarsari-depok-dekat-tol.html                         
    650     72    70       http://rumahdijual.com/depok/893318-perumahan-orchid-green-village.html                                            
    650     72    60       http://rumahdijual.com/depok/1040570-rumah-nyaman-aman-dan-adem-di-grand-depok-city.html                           
    650     72    60       http://rumahdijual.com/depok/1030026-rumah-strategis-di-grand-depok-city.html                                      
    650     72    50       http://rumahdijual.com/depok/1283955-rumah-dekat-gran-city-depok-siap-huni-murah-strategis.html                    
    650     72    43       http://rumahdijual.com/depok/1260367-jual-rumah-dekat-u-i-depok.html                                               
    650     72    40       http://rumahdijual.com/depok/1156805-dijual-rumah-siap-huni-cluster-puri-radensa-depok.html                        
    650     72    36       http://rumahdijual.com/depok/765118-dijual-rumah-bella-casa-residence-depok.html                                   
    650     105   69       http://rumahdijual.com/depok/1038050-rumah-murah-tanah-luas-lokasi-super-strategis.html                            
    650     105   65       http://rumahdijual.com/depok/824413-2-unit-terakhir-ready-stock.html                                               
    650     105   45       http://rumahdijual.com/depok/1300818-rumah-cantik-minimalis-di-tanah-baru-beji-ready-stock.html                    
    650     103   58       http://rumahdijual.com/depok/1309812-rumah-nyaman-di-mutiara-residence-poncol-beji-depok.html                      
    650     103   58       http://rumahdijual.com/depok/1306718-rumah-minimalis-di-tanah-baru-depok.html                                      
    650     103   50       http://rumahdijual.com/depok/947689-mutiara-residence-lokasi-tanah-baru-depok.html                                 
    650     101   60       http://rumahdijual.com/depok/1250879-rumah-mungil-di-depok.html                                                    
    650     100   75       http://rumahdijual.com/depok/976478-rumah-murah-2-lantai-depok-timur.html                                          
    650     100   75       http://rumahdijual.com/depok/948247-cluster-bunga-geulis.html                                                      
    650     100   75       http://rumahdijual.com/depok/1299452-rumah-cantik-masuk-mobil-di-kalimulya-depok-r21-0489-a.html                   
    655     95    75       http://rumahdijual.com/depok/836480-rumah-pojokan-cluster-120-m-dr-angkot-d-105-a.html                             
    655     90    45       http://rumahdijual.com/depok/945332-rumah-ready-siap-huni-di-depok.html                                            
    655     84    60       http://rumahdijual.com/depok/898936-jual-rumah-siap-huni.html                                                      
    655     75    45       http://rumahdijual.com/depok/1226812-rumah-cluster-baru-dan-siap-huni-di-limo-cinere.html                          
    655     72    30       http://rumahdijual.com/depok/459007-rumah-minimalis-dan-nyaman-di-depok-permata-cimanggis.html                     
    655     68    70       http://rumahdijual.com/depok/1291424-basement-berlian-cluster-unik-kpr-dp-ringan-proses-dibantu.html               
    655     105   70       http://rumahdijual.com/depok/1110118-rumah-siap-huni-di-komplek.html                                               
    655     100   70       http://rumahdijual.com/depok/689524-murah-luas-strategis.html                                                      
    657     78    40       http://rumahdijual.com/depok/320297-perumahan-di-depok-dekat-stasiun-tanah-baru-depok-green.html                   
    657     101   60       http://rumahdijual.com/depok/721783-dapatkan-fasilitas-bonus-rumah-pantas-unit-terbatas-studio-alam.html           
    658     82    55       http://rumahdijual.com/depok/1300967-rumah-murah-di-tanah-baru-beji-siap-huni-bebas.html                           
    660     97    75       http://rumahdijual.com/depok/1160447-rumah-murah-cluster-tanah-baru-5-menit-dr-pintu.html                          
    660     97    74       http://rumahdijual.com/depok/1160454-rumah-murah-siap-huni-dan-kor-cluster-120-m.html                              
    660     96    60       http://rumahdijual.com/depok/1047166-rumah-dijual-di-depok-tanah-baru-murah.html                                   
    660     96    60       http://rumahdijual.com/depok/1029033-rumah-dijual-di-tanah-baru-curug-depok-lokasi-di.html                         
    660     96    54       http://rumahdijual.com/depok/1109213-hunian-cantik-di-depok-diskon-dp-70-a.html                                    
    660     96    54       http://rumahdijual.com/depok/1128882-rumah-modern-minimalis-lokasi-strategis-halaman-luas-di-depok.html            
    660     96    54       http://rumahdijual.com/depok/1130221-rumah-minimalis-type-54-96-lokasi-sangat-strategis.html                       
    660     85    62       http://rumahdijual.com/depok/1158416-rumah-manis-minimalis-cluster-120-m-dr-angkot-d.html                          
    660     80    58       http://rumahdijual.com/depok/886266-jual-3-unit-rumah-jarang-ada-nempel-kota-depok.html                            
    660     65    70       http://rumahdijual.com/depok/1312145-rumah-mungil-dekat-tol-cijago-tanah-baru-depok.html                           
    660     103   60       http://rumahdijual.com/depok/919379-rumah-di-jl-studio-alam-depok.html                                             
    660     103   50       http://rumahdijual.com/depok/721948-di-jual-rumah-cantik-siap-huni-permata-regency-depok.html                      
    660     100   60       http://rumahdijual.com/depok/731202-cluster-mandor-ety.html                                                        
    665     89    65       http://rumahdijual.com/depok/1024825-di-jual-rumah-baru-cuantik-siap-huni-di-kalimulya.html                        
    665     88    45       http://rumahdijual.com/depok/1075742-rumah-dengan-gaya-arsitektur-yang-unik-tamanna-townhouse-sawangan.html        
    665     88    45       http://rumahdijual.com/depok/959252-hunian-exclusive-lokasi-strategis-bisa-kpr-di-sawangan-depok.html              
    667     84    56       http://rumahdijual.com/depok/1026411-rumah-kecil-dlm-cluster-dp-murah-di-tanahbaru-depok.html                      
    667     84    56       http://rumahdijual.com/depok/1232040-rasheesa-2-hunian-nyaman-nyaman-harga-teman.html                              
    667     84    56       http://rumahdijual.com/depok/902088-hunian-idaman-di-lokasi-strategis-nyaman-dan-aman.html                         
    667     84    56       http://rumahdijual.com/depok/862362-cluster-nyaman-lokasi-dekat-grand-depok-city.html                              
    667     84    56       http://rumahdijual.com/depok/1226463-rasheesa-2-hunian-nyaman-lokasi-super-strategis.html                          
    667     84    56       http://rumahdijual.com/depok/774624-cluster-cantik-free-legallitas-dp-di-cicil-lokasi-selangkah.html               
    667     84    56       http://rumahdijual.com/depok/1209075-hunian-exclusive-di-pusat-kota-depok-10-menit-stasiun.html                    
    667     84    50       http://rumahdijual.com/depok/1121038-beli-rumah-dapat-kan-disount-akhir-tahun-di-depok.html                        
    668     92    55       http://rumahdijual.com/depok/997446-rumah-murah-strategis-di-jl-h-sofyan-radar-auri.html                           
    669     74    38       http://rumahdijual.com/depok/1104273-rumah-murah-dp-suka-suka-di-cimanggis.html                                    
    669     72    38       http://rumahdijual.com/depok/1015731-dijual-rumah-sangat-strategis-akses-2-tol-cijago-cibubur.html                 
    669     72    38       http://rumahdijual.com/depok/953845-rumah-cantik-akses-tol-cibubur-dan-cijago-cimanggis-depok.html                 
    670     99    45       http://rumahdijual.com/depok/1014363-cluster-cinangka-saatnya-mudah-dapat-rumah.html                               
    670     94    36       http://rumahdijual.com/depok/1067111-rumah-di-grand-depok-city-cluster-anggrek.html                                
    670     90    70       http://rumahdijual.com/depok/695003-di-jual-rumah-cantik-siap-huni-di-dekat-stasiun.html                           
    670     90    60       http://rumahdijual.com/depok/928199-rumah-di-grand-depok-city.html                                                 
    670     73    42       http://rumahdijual.com/depok/1114732-rumah-clutser-beji-dekat-tanah-baru-lokasi-strategis-nyaman.html              
    670     73    42       http://rumahdijual.com/depok/984140-cluster-di-pinggir-jalan-beji-tanah-baru-depok.html                            
    670     73    42       http://rumahdijual.com/depok/985882-cluster-minimalis-di-tanah-baru-depok.html                                     
    670     73    42       http://rumahdijual.com/depok/915878-cluster-mewah-harga-terjangkau-di-beji-depok.html                              
    670     73    42       http://rumahdijual.com/depok/973298-cluster-cantik-di-beji-tanah-baru-depok.html                                   
    670     73    42       http://rumahdijual.com/depok/1099400-rumah-cluster-di-daerah-beji-depok.html                                       
    670     73    42       http://rumahdijual.com/depok/894194-rumah-cluster-di-beji-tanah-baru-depok.html                                    
    670     73    42       http://rumahdijual.com/depok/902985-rumah-murah-di-depok.html                                                      
    670     73    42       http://rumahdijual.com/depok/893825-di-jual-cluster-di-beji-tanah-baru-depok.html                                  
    670     73    42       http://rumahdijual.com/depok/1099421-rumah-second-kondisi-prima-dalam-cluster-di-beji-tanah.html                   
    670     105   47       http://rumahdijual.com/depok/1211293-rumah-sawangan-indah-siap-huni.html                                           
    671     91    45       http://rumahdijual.com/depok/583705-rumah-ready-stock-dp-20-jutaan-di-depok.html                                   
    671     91    45       http://rumahdijual.com/depok/586518-rumah-ready-stock-dp-20-jutaan.html                                            
    673     83    45       http://rumahdijual.com/depok/1222781-andaru-insani-residence-hunian-exclusive-dan-asri.html                        
    675     99    55       http://rumahdijual.com/depok/983535-jual-rumah-bagus-mulus-siap-huni-tanpa-renovasi-di.html                        
    675     97    50       http://rumahdijual.com/depok/1144864-nuansa-asri-cinangka-sawangan-depok.html                                      
    675     95    60       http://rumahdijual.com/depok/1307025-rumah-minimalis-tanah-baru.html                                               
    675     94    36       http://rumahdijual.com/depok/1067165-rumah-di-grand-depok-city.html                                                
    675     90    60       http://rumahdijual.com/depok/1291669-dijual-rumah-indent-di-beji-depok-kavling-ui-barat.html                       
    675     90    60       http://rumahdijual.com/depok/1281620-dijual-rumah-kavling-ui-barat-beji-depok.html                                 
    675     84    70       http://rumahdijual.com/depok/972554-rumah-dekat-tol-dikontrakkan.html                                              
    675     84    60       http://rumahdijual.com/depok/1260365-rumah-di-grand-depok-city.html                                                
    675     84    55       http://rumahdijual.com/depok/892315-rumah-dijual-dekat-dengan-tol-cijago-tol-cibubur.html                          
    675     84    50       http://rumahdijual.com/depok/1076761-rumah-keluarga-harmonis.html                                                  
    675     79    72       http://rumahdijual.com/depok/941356-rumah-adem-bikin-nyaman.html                                                   
    675     76    36       http://rumahdijual.com/depok/968813-dijual-rumah-di-villa-tanah-baru-beji-depok.html                               
    675     76    36       http://rumahdijual.com/depok/820092-rumah-cluster-di-tanah-baru-depok.html                                         
    675     73    42       http://rumahdijual.com/depok/1099511-cluster-murah-di-beji.html                                                    
    675     72    45       http://rumahdijual.com/depok/1051687-rumah-baru-tempati-dijual-mau-pindah.html                                     
    675     105   50       http://rumahdijual.com/depok/1029219-rumah-siap-masuk-di-pondok-rajeg.html                                         
    678     84    45       http://rumahdijual.com/depok/596448-permata-cimanggis-depok.html                                                   
    678     84    45       http://rumahdijual.com/depok/760857-permata-cimanggis.html                                                         
    678     84    45       http://rumahdijual.com/depok/624742-rumah-murah-di-depok-permata-cimanggis-003-a.html                              
    678     105   45       http://rumahdijual.com/depok/625978-rumah-murah-di-depok-permata-cimanggis-004-a.html                              
    680     90    60       http://rumahdijual.com/depok/1125535-rumah-nyaman-dekat-stasiun.html                                               
    680     90    60       http://rumahdijual.com/depok/899227-rumah-nyaman-murah-dekat-stasiun.html                                          
    680     90    45       http://rumahdijual.com/depok/709099-di-jual-rumah-di-perumahan-gdc-depok.html                                      
    680     90    36       http://rumahdijual.com/depok/576851-rumah-di-grand-depok-city.html                                                 
    680     85    55       http://rumahdijual.com/depok/1140949-rumah-minimalis-sangat-strategis-deket-margonda-dan-universitas-indonesia.html
    680     84    55       http://rumahdijual.com/depok/867838-momien-residence-hunian-nyentrik-desain-unik-dan-diskon-menark.html            
    680     84    45       http://rumahdijual.com/depok/1282975-jual-bu-rumah-di-pinggir-tol-cijago-cibubur-dkt.html                          
    680     84    45       http://rumahdijual.com/depok/1027904-rumah-asri-murah-strategis-free-biaya2.html                                   
    680     84    45       http://rumahdijual.com/depok/760848-permata-cimanggis.html                                                         
    680     84    45       http://rumahdijual.com/depok/586333-rumah-murah-45-84-di-depok-permata-cimanggis.html                              
    680     84    36       http://rumahdijual.com/depok/1068327-di-jual-rumah-baru-minimalis-siap-huni-di-lokasi.html                         
    680     83    55       http://rumahdijual.com/depok/1257270-cluster-momien-residence-lokasi-tanah-baru.html                               
    680     80    60       http://rumahdijual.com/depok/1123925-minimalis-nuansa-tropis-dekat-stasiun.html                                    
    680     80    60       http://rumahdijual.com/depok/1146962-rumah-nyaman-akses-mudah.html                                                 
    680     80    60       http://rumahdijual.com/depok/1114374-minimalis-nuansa-tropis-dekat-stasiun.html                                    
    680     80    60       http://rumahdijual.com/depok/1122112-minimalis-nuansa-tropis-dekat-stasiun.html                                    
    680     80    55       http://rumahdijual.com/depok/1285732-cluster-momien-lokasi-terdepan-dp-ringan-proses-kpr-dibantu.html              
    680     80    55       http://rumahdijual.com/depok/946325-hunian-nyentrik-dengan-desain-unik-di-tanah-baru-depok.html                    
    680     80    55       http://rumahdijual.com/depok/1091700-rumah-ready-stock-tipe-55-80-di-tanah-baru.html                               
    680     80    55       http://rumahdijual.com/depok/1047026-hunian-nyentrik-dengan-desain-unik-di-tanah-baru.html                         
    680     80    55       http://rumahdijual.com/depok/934465-cluster-momien-residence-lokasi-strategis-kepleset-sampai-ke-ui.html           
    680     72    45       http://rumahdijual.com/depok/989236-dijual-rumah-puri-depok-mas.html                                               
    680     72    36       http://rumahdijual.com/depok/1068337-di-jual-rumah-baru-minimalis-siap-huni-di-taman.html                          
    680     105   48       http://rumahdijual.com/depok/909500-botania-lake-residence-hunian-premium-bernuansa-resort-sawangan.html           
    680     105   45       http://rumahdijual.com/depok/731527-rumah-dilingkungan-asri-dan-nyaman-di-depok.html                               
    680     102   70       http://rumahdijual.com/depok/893520-rumah-murah-di-depok-dalam-perumahan.html                                      
    680     102   54       http://rumahdijual.com/depok/971553-rumah-komplek-sawangan-permai-nyaman-luas-lokasi-strategis.html                
    680     102   48       http://rumahdijual.com/depok/970424-rumah-murah-di-sawangan-permai.html                                            
    680     102   48       http://rumahdijual.com/depok/1280892-rumah-murah-dan-nyaman-di-daerah-komplek-sawangan-permai.html                 
    680     102   48       http://rumahdijual.com/depok/1119098-rumah-murah-di-sawangan-permai-depok.html                                     
    680     102   48       http://rumahdijual.com/depok/928586-rumah-dijual-sawangan-permai-depok.html                                        
    680     102   48       http://rumahdijual.com/depok/920605-rumah-di-komplek-sawangan-permai-nyaman-murah-meriah-segera.html               
    680     102   48       http://rumahdijual.com/depok/932375-rumah-komplek-sawangan-permai-nyaman-luas-lokasi-strategis.html                
    680     102   48       http://rumahdijual.com/depok/981565-rumah-dijual-di-sawangan-nyaman-strategis-680-jt.html                          
    680     102   48       http://rumahdijual.com/depok/1117495-rumah-murah-terawat-siap-huni.html                                            
    680     102   48       http://rumahdijual.com/depok/916314-rumah-komplek-sawangan-lokasi-strategis-dan-nyaman.html                        
    680     102   48       http://rumahdijual.com/depok/970421-rumah-dijual-di-sawangan-permai.html                                           
    680     102   48       http://rumahdijual.com/depok/937321-jual-rumah-murah-di-sawangan-depok-harga-680-juta.html                         
    680     102   48       http://rumahdijual.com/depok/923283-rumah-komplek-sawangan-permai-lokasi-strategis-murah-meriah.html               
    680     100   60       http://rumahdijual.com/depok/1136362-rumah-second-terbaik-di-kelasnya-dekat-cinere-depok.html                      
    683     90    36       http://rumahdijual.com/depok/1094262-depok-jl-margonda-raya-perumahan-grand-depok-city.html                        
    685     96    60       http://rumahdijual.com/depok/1061027-rumah-di-tanah-baru-curug-agung-depok.html                                    
    685     93    45       http://rumahdijual.com/depok/1202847-depok-raden-sanim-tanah-baru-rumah-cantik-menarik-siap.html                   
    685     90    60       http://rumahdijual.com/depok/1117638-rumah-minimalis-dan-cantik-harga-ekonomis.html                                
    685     88    50       http://rumahdijual.com/depok/872160-dijual-rumah-desain-unik-harga-minimalis-sawangan.html                         
    688     94    55       http://rumahdijual.com/depok/850363-momien-residence-cluster-minimalis-selangkah-ke-jakarta-blkng-kampus.html      
    690     98    60       http://rumahdijual.com/depok/1191720-rumah-depok-sawangan-60-98-ready-stock-bisa-kpr.html                          
    690     93    70       http://rumahdijual.com/depok/614248-rumah-cluster-di-depok-curug-agung.html                                        
    690     93    70       http://rumahdijual.com/depok/1120268-rumah-baru-mini-cluster-lokasi-strategis-di-tanah-baru.html                   
    690     93    70       http://rumahdijual.com/depok/979020-rumah-dlm-cluster-di-tanah-baru-beji-depok.html                                
    690     86    75       http://rumahdijual.com/depok/1265655-rumah-2-lantai-di-cimanggis-depok.html                                        
    690     70    56       http://rumahdijual.com/depok/1095966-rumah-bernuansa-taman-dan-relegius.html                                       
    690     100   66       http://rumahdijual.com/depok/955939-rumah-cantik-dan-murraahh-di-lokasi-dekat-depok.html                           
    695     72    45       http://rumahdijual.com/depok/1247305-jual-rumah-minimalis-dan-strategis-di-tanah-baru-depok.html                   
    695     60    60       http://rumahdijual.com/depok/1279368-rumah-asri-exlusive-di-cibubur-di-apit-dua-tol.html                           
    699     84    61       http://rumahdijual.com/depok/822638-rumah-siap-huni-di-bojongsari-depok.html                                       
    699     84    49       http://rumahdijual.com/depok/822786-rumah-1-lantai-ready-stock-di-bojongsari-depok.html                            
    699     84    49       http://rumahdijual.com/depok/779165-rumah-siap-huni-di-depok-2015-a.html                                           
    699     84    49       http://rumahdijual.com/depok/849586-rumah-minimalis-ready-stock-di-depok.html                                      
    699     84    49       http://rumahdijual.com/depok/1019737-rumah-sederhana-di-bojongsari.html                                            
    699     84    49       http://rumahdijual.com/depok/940917-rumah-siap-huni-di-serua-depok.html                                            
    699     84    49       http://rumahdijual.com/depok/1012675-rumah-ready-stock-1-lantai-di-bojongsari.html                                 
    699     84    49       http://rumahdijual.com/depok/998558-rumah-sederhana-di-bojongsari.html                                             
    700     99    65       http://rumahdijual.com/depok/1089053-rumah-minimalis-semi-furnished.html                                           
    700     98    75       http://rumahdijual.com/depok/1174331-dijual-rumah-tanpa-prantara.html                                              
    700     98    75       http://rumahdijual.com/depok/732182-rumah-cantik-harga-menarik-di-raden-saleh.html                                 
    700     98    60       http://rumahdijual.com/depok/1124363-rumah-cluster-di-tanah-baru-depok.html                                        
    700     96    70       http://rumahdijual.com/depok/1031253-cluster-cantik-di-kalimulya-depok-r21-0325-a.html                             
    700     95    54       http://rumahdijual.com/depok/770585-rumah-memukau-harga-terjangkau-cluster-kalimulya.html                          
    700     92    70       http://rumahdijual.com/depok/777875-hunian-dekat-dengan-fasilitas-umum-kualitas-premium-di-pesona.html             
    700     91    49       http://rumahdijual.com/depok/606367-rumah-cluster-28-unit-di-serua-depok-dp-cicil.html                             
    700     90    50       http://rumahdijual.com/depok/1254723-bu-jual-cepat-perumahan-nuansa-asri-semi-furnish.html                         
    700     90    45       http://rumahdijual.com/depok/658258-rumah-cluster-kota-depok-bisa-request.html                                     
    700     90    45       http://rumahdijual.com/depok/1048130-rumah-mewah-harga-murah-di-depok.html                                         
    700     90    36       http://rumahdijual.com/depok/1307932-depok-margonda-raya-jl-ra-kartini-perumahan-grand-depok.html                  
    700     89    75       http://rumahdijual.com/depok/1031075-cluster-wisma-8-beji.html                                                     
    700     88    70       http://rumahdijual.com/depok/1166607-rumah-depok-mewah-murah-cimanggis.html                                        
    700     88    64       http://rumahdijual.com/depok/1306331-rumah-murah-di-taman-anggrek-3-cinere.html                                    
    700     88    54       http://rumahdijual.com/depok/1279224-jual-mudah-bekal-pindah.html                                                  
    700     87    60       http://rumahdijual.com/depok/1135703-dijual-over-credit-rumah-pear-garden-cimanggis-blok-d14.html                  
    700     85    64       http://rumahdijual.com/depok/902431-rumah-baru-didalam-cluster-di-griya-cinere.html                                
    700     84    49       http://rumahdijual.com/depok/1163944-trevista-serua-residence-sawangan.html                                        
    700     80    60       http://rumahdijual.com/depok/1160444-rumah-manis-semi-furnished-cluster-5-menit-dr-pintu.html                      
    700     79    67       http://rumahdijual.com/depok/1160377-rumah-minimalis-dekat-stasiun-kereta-depok-di-pitara-green.html               
    700     79    60       http://rumahdijual.com/depok/934463-rumah-cluster-di-jual-di-kelapa-dua-depok.html                                 
    700     78    70       http://rumahdijual.com/depok/1174339-rumah-termurah-di-cimanggis-depok.html                                        
    700     78    70       http://rumahdijual.com/depok/1174397-rumah-termurah-di-cimanggis-depok.html                                        
    700     78    60       http://rumahdijual.com/depok/1299974-dijual-rumah-di-beji-depok-2-lantai.html                                      
    700     78    40       http://rumahdijual.com/depok/983507-dijual-cepat-tanpa-perantara-di-panorama-residence.html                        
    700     77    68       http://rumahdijual.com/depok/1185401-rumah-di-jual-bu-di-cinere-depok.html                                         
    700     74    65       http://rumahdijual.com/depok/709688-dijual-rumah-siap-huni-dalam-komplek.html                                      
    700     72    72       http://rumahdijual.com/depok/1241298-murah-jual-cepat-bu-rumah-cinere.html                                         
    700     72    68       http://rumahdijual.com/depok/1130202-rumah-dicinere-strategis.html                                                 
    700     72    68       http://rumahdijual.com/depok/1155355-rumah-murah-dicinere.html                                                     
    700     72    68       http://rumahdijual.com/depok/1162779-rumah-bagus-harga-murah-di-daerah-cinere.html                                 
    700     72    50       http://rumahdijual.com/depok/1223470-investasi-terbaik-dengan-properti.html                                        
    700     70    65       http://rumahdijual.com/depok/1019465-rumah-minimalis-2-lantai-tanah-baru.html                                      
    700     105   48       http://rumahdijual.com/depok/579267-rumah-mewah-harga-murah-botania-lake.html                                      
    700     105   45       http://rumahdijual.com/depok/843988-rumah-murah-type-45-105-di-cimanggis-bebas-banjir.html                         
    700     105   38       http://rumahdijual.com/depok/590888-rumah-cantik-siap-huni-taman-sari-puri-bali-sawangan.html                      
    700     101   70       http://rumahdijual.com/depok/1081017-rumah-siap-huni-di-tanah-baru-depok-r21-0382-a.html                           
    700     101   70       http://rumahdijual.com/depok/1276700-dijual-rumah-di-kawasan-sukma-jaya-desain-bagus-harga.html                    
    700     101   70       http://rumahdijual.com/depok/1279971-dijual-cepat-dan-murah-di-kawasan-sukmajaya-depok.html                        
    700     100   65       http://rumahdijual.com/depok/837418-rumah-pinggir-ui-dan-deket-margonda-depok.html                                 
    700     100   60       http://rumahdijual.com/depok/914188-rumah-minimalis-cinere-limo.html                                               
    700     100   60       http://rumahdijual.com/depok/917688-rumah-minimalis-cinere-limo.html                                               
    700     100   48       http://rumahdijual.com/depok/948703-rumah-asri-siap-huni-di-tamansari-puri-bali.html
    

## House Price Between 750 - 800 Mio IDR

### Visualize Data


```python
df = visualizeData('depok', 750, 800);
```


![png](png/output_68_0.png)


### Analyze the Data of House Price Between 750 - 800 Mio IDR


```python
avg = averageMeasures(df)
```

    
    AVERAGE MEASURES
    -----------------
    
    building    89
        land   121
       price   774
    


```python
mostSpacious(df)
```

    
    MOST SPACIOUS LAND
    -----------------
    
        bath     2
         bed     3
    building   120
        land   550
       price   800
         url   http://rumahdijual.com/depok/907483-rumah-suasana-villa-pedesaan.html
    
    MOST SPACIOUS BUILDING
    -----------------
    
        bath     2
         bed     3
    building   240
        land   120
       price   800
         url   http://rumahdijual.com/depok/508232-rumah-di-depok-mampang.html
    


```python
selectEconomical(df, avg, unit)
```

    
    MOST ECONOMICAL
    -----------------
    is when the price is really below average: 774 (million IDR) but you get above the average land: 121 (square meters) and above the average building: 89 (square meters)
    
    You are blessed to choose one of these 38  houses:
    
    price  land building                                                                                                      url
    750     425   150      http://rumahdijual.com/depok/825781-rumah-kebun-kos-kosan-tanah-luas-di-kota-depok.html               
    750     350   150      http://rumahdijual.com/depok/881926-rumah-murah-plus-kontrakan-3-pintu-di-depok.html                  
    750     335   100      http://rumahdijual.com/depok/1062544-dijual-rumah-asri-dicinangka-sawangan-depok.html                 
    750     254   150      http://rumahdijual.com/depok/802417-rumah-kontrakan-5-pintu-sangat-strategis-buat-investasi.html      
    750     230   120      http://rumahdijual.com/depok/1188323-dijual-rumah-di-villa-pertiwi-depok.html                         
    750     225   150      http://rumahdijual.com/depok/1056159-rumah-murah-di-depok-2-tengah.html                               
    750     207   90       http://rumahdijual.com/depok/1065226-rumah-siap-huni-tanah-luas-bangunan-lux.html                     
    750     207   150      http://rumahdijual.com/depok/1057019-rumah-di-depok-pitara.html                                       
    750     207   130      http://rumahdijual.com/depok/1040992-rumah-siap-huni-luas-full-granite-harga-boleh-di.html            
    750     207   130      http://rumahdijual.com/depok/1075716-rumah-luas-full-granit-dan-banyak-bonusnya-di-pitara.html        
    750     206   150      http://rumahdijual.com/depok/526946-rumah-cantik-harga-pas-di-pancoran-mas.html                       
    750     200   190      http://rumahdijual.com/depok/748387-kos-kos-murah-dan-produktif-di-kukusan-beji-depok.html            
    750     200   180      http://rumahdijual.com/depok/748398-rumah-tinggal-dan-kontrakan-di-tanah-baru-depok.html              
    750     200   150      http://rumahdijual.com/depok/727257-kontrakan-3-pintu-ratu-jaya-depok.html                            
    750     200   100      http://rumahdijual.com/depok/1057854-rumah-luas-harga-di-jamin-pas.html                               
    750     187   100      http://rumahdijual.com/depok/1081635-murah-jarang-ada-bisa-kpr-rumah-cantik-siap-huni.html            
    750     180   150      http://rumahdijual.com/depok/1077655-rumah-di-jual-di-depok-timur.html                                
    750     175   125      http://rumahdijual.com/depok/1300657-rumah-di-depok-cilodong-belakang-perumahan-marco.html            
    750     170   150      http://rumahdijual.com/depok/972012-kavling-abdul-wahab-jangan-ragu-ambil-keputusan.html              
    750     170   150      http://rumahdijual.com/depok/850847-rumah-plus-toko-di-tanah-baru-beji.html                           
    750     168   155      http://rumahdijual.com/depok/788631-rumah-dijual-murah-di-tanah-baru-depok.html                       
    750     160   200      http://rumahdijual.com/depok/466547-jual-rumah-tingkat-lt-160m-di-tigaputra-meruyung-limo.html        
    750     160   130      http://rumahdijual.com/depok/885759-rumah-margonda-belakang-kampus-bsi.html                           
    750     150   90       http://rumahdijual.com/depok/1056054-perumahan-depok-jalan-raya-pitara-depok.html                     
    750     150   100      http://rumahdijual.com/depok/850075-rumah-cocok-untuk-kontrakan-lokasi-samping-ciganjur-jaksel.html   
    750     147   90       http://rumahdijual.com/depok/1248622-pamulang-village-depok-light-up-your-family-ties.html            
    750     144   200      http://rumahdijual.com/depok/391777-rumah-poin-mas-pancoran-mas.html                                  
    750     135   110      http://rumahdijual.com/depok/984602-rumah-di-cilangkap-banjaran-pucung-kota-depok.html                
    750     130   200      http://rumahdijual.com/depok/762723-rumah-dijual-murah-di-sawangan-depok.html                         
    750     130   110      http://rumahdijual.com/depok/1073476-rumah-daerah-depok.html                                          
    750     130   110      http://rumahdijual.com/depok/902153-rumah-second-beji.html                                            
    750     125   90       http://rumahdijual.com/depok/1159269-rumah-perumnas-nyaman-tenang-dekat-dengan-angkot-lebar-jalan.html
    750     125   102      http://rumahdijual.com/depok/725911-perum-audita-1-sawangan-depok.html                                
    750     124   115      http://rumahdijual.com/depok/1098123-rumah-di-jual-cepat-karena-mau-pindah.html                       
    750     122   98       http://rumahdijual.com/depok/1231108-rumah-siap-huni-suasana-asri-dan-sejuk.html                      
    750     122   92       http://rumahdijual.com/depok/655018-rumah-dijual-hunian-asri-di-cimanggis-depok-10-menit.html         
    770     197   125      http://rumahdijual.com/depok/1257839-rumah-dijual-mekarsari-cimanggis-depok.html                      
    770     134   105      http://rumahdijual.com/depok/908185-rumah-siap-pakai-perumahan-faria-mampang-depok.html
    


```python
selectModerate(df, avg, unit)
```

    
    MODERATE PRICE
    -----------------
    is when the price is above average: 774 (million IDR) with above-average land: 121 (square meters) and above-average building: 89 (square meters)
    
    
    There are : 74  items with above-average price and above-average land.
    
    There are : 45  items with above-average price, above-average land and above-average building.
    
    price  land building                                                                                                     url
    775     300   150      http://rumahdijual.com/depok/1089285-rumah-besar-beserta-kontrakan-2-pintu-di-sawangan.html          
    775     152   90       http://rumahdijual.com/depok/1232445-rumah-siap-huni-di-grand-depok-city-r21-0437-a.html             
    775     149   95       http://rumahdijual.com/depok/1232504-cluster-grand-depok-city-dekat-stasiun-depok-r21-0438-a.html    
    779     152   152      http://rumahdijual.com/depok/1021544-rumah-nyaman-tentram-dan-indah.html                             
    780     150   110      http://rumahdijual.com/depok/1192055-wisma-mas-pondok-cabe.html                                      
    785     220   130      http://rumahdijual.com/depok/677163-rumah-teduh-nan-harmoni-di-depok.html                            
    785     132   100      http://rumahdijual.com/depok/962952-di-jual-rumah-asri-cantik-di-pondok-rajeg-depok.html             
    790     290   190      http://rumahdijual.com/depok/1058497-apakah-anda-menginginkan-rumah-yang-bernuansa-asri-dan-jauh.html
    790     130   90       http://rumahdijual.com/depok/1268021-di-jual-cluster-cemara-dgn-harga-murah-desain-2lantai.html      
    799     300   150      http://rumahdijual.com/depok/1196401-sawangan-lt-300-m2-800-juta.html                                
    799     125   100      http://rumahdijual.com/depok/1153879-bukit-rivaria-800-juta-2-lantai.html                            
    800     550   165      http://rumahdijual.com/depok/900849-dijual-rumah-kebun-hijau-shm-imb-cagar-alam-depok.html           
    800     550   120      http://rumahdijual.com/depok/907483-rumah-suasana-villa-pedesaan.html                                
    800     396   112      http://rumahdijual.com/depok/1097593-rumah-kebayunan-tapos-depok.html                                
    800     316   200      http://rumahdijual.com/depok/1027682-1-rumah-tinggal-beserta-5-pintu-kontrakan.html                  
    800     220   220      http://rumahdijual.com/depok/914554-dijual-rumah-di-sawangan-depok.html                              
    800     220   100      http://rumahdijual.com/depok/864729-rumah-minimalis-siap-huni-asri-murah-di-cinangka-sawangan.html   
    800     207   150      http://rumahdijual.com/depok/1069233-rumah-cluster-207m2-strategis-depok.html                        
    800     207   150      http://rumahdijual.com/depok/1283761-rumah-murah-masuk-mobil-di-depok-r21-0477-a.html                
    800     207   130      http://rumahdijual.com/depok/1073540-rumah-mewah-harga-sederhana-dekat-jalan-raya-depok-rute.html    
    800     205   120      http://rumahdijual.com/depok/1158141-rumah-second-siap-huni-murah-di-depok.html                      
    800     205   100      http://rumahdijual.com/depok/908110-rumah-second-minimalis-siap-huni-di-kelapa-2-depok.html          
    800     203   94       http://rumahdijual.com/depok/1015987-rumah-dikawasan-depok-lama-pancoran-dekat-st-depok-lama.html    
    800     200   90       http://rumahdijual.com/depok/910947-dijual-rumah-tinggal-di-depok-view-menarik-tp.html               
    800     199   160      http://rumahdijual.com/depok/1258118-rumah-luas-nyaman-dekat-matoa-golf-tanah-baru-ada.html          
    800     195   157      http://rumahdijual.com/depok/1035757-rumah-murah-dan-strategis-pondok-cina-depok.html                
    800     190   170      http://rumahdijual.com/depok/1065094-jual-cepat-rumah-di-depok.html                                  
    800     185   90       http://rumahdijual.com/depok/1056045-rumah-minimalis-di-kali-mulya-depok.html                        
    800     185   130      http://rumahdijual.com/depok/1212455-dijual-rumah-second-bu.html                                     
    800     182   130      http://rumahdijual.com/depok/1185312-dijual-cepat-rumah-second-pancoran-mas-depok.html               
    800     179   140      http://rumahdijual.com/depok/1194047-rumah-luas-dan-strategis-di-depok-timur.html                    
    800     176   150      http://rumahdijual.com/depok/853730-rumah-murah-tanah-ngantong-luas-pekapuran-depok.html             
    800     175   105      http://rumahdijual.com/depok/1193953-dijual-rumah-di-margonda-depok-cocok-untuk-rumah-kos.html       
    800     171   145      http://rumahdijual.com/depok/1119458-hunian-asri-dan-nyaman-di-pinggir-kota.html                     
    800     170   150      http://rumahdijual.com/depok/903688-rumah-dijual-cepat.html                                          
    800     167   150      http://rumahdijual.com/depok/900594-dijual-rumah-kios-siap-huni-hanya-3-menit-ke.html                
    800     155   125      http://rumahdijual.com/depok/1268588-rumah-strategis-investasi-cerdas-masa-depan-di-sawangan.html    
    800     154   100      http://rumahdijual.com/depok/1179110-rumah-dijual-depok-baru-maharaja-2016-a.html                    
    800     154   100      http://rumahdijual.com/depok/1145096-rumah-dijual-depok-murah-pancoran-mas.html                      
    800     150   120      http://rumahdijual.com/depok/904257-rumah-pinggir-jalan-di-beji-depok.html                           
    800     150   100      http://rumahdijual.com/depok/1050020-rumah-di-tengsh-komplek.html                                    
    800     137   137      http://rumahdijual.com/depok/899981-rumah-di-jual-di-villa-pertiwi.html                              
    800     131   98       http://rumahdijual.com/depok/972377-rumah-siap-huni-dijual-cepat.html                                
    800     127   120      http://rumahdijual.com/depok/739432-rumah-baru-2-lantai-siap-huni-beji-depok.html                    
    800     125   160      http://rumahdijual.com/depok/598845-rumah-lux-di-kampung-di-rawa-denok-pancoran-mas.html
    


```python
selectExpensive(df, avg, unit)
```

    
    EXPENSIVE PRICE
    -----------------
    is when the price is above average: 774 (million IDR) but you only get land below average: 121 (square meters) and building below average: 89 (square meters).
    
    
    
    There are : 126  items that matched the EXPENSIVE category.
    
    price  land building                                                                                                        url
    775     90    80       http://rumahdijual.com/depok/1118654-rumah-di-permata-arcadia-cimanggis-depok-akses-tol-dan.html        
    775     90    75       http://rumahdijual.com/depok/1259553-kotak-kembang-depok-raya.html                                      
    775     90    72       http://rumahdijual.com/depok/1276035-siap-huni-siap-nego-kpr-dibantu-buruan.html                        
    775     90    72       http://rumahdijual.com/depok/1280082-rumah-cantik-dengan-harga-terjangkau-negotiable.html               
    775     87    69       http://rumahdijual.com/depok/1066712-dijual-rumah-siap-huni-di-depok.html                               
    775     80    60       http://rumahdijual.com/depok/926790-rumah-strategis-akses-mudah-di-kelapa-dua-depok.html                
    775     62    75       http://rumahdijual.com/depok/1188432-rumah-baru-2-lantai-cluster-yg-nyaman-di-kukusan.html              
    775     120   36       http://rumahdijual.com/depok/1141606-rumah-fresh-n-orisinil-anggrek-2-grand-depok-city.html             
    775     110   60       http://rumahdijual.com/depok/896878-umah-dijual-krukut-rumah-residence-tenang-nyaman.html               
    778     99    60       http://rumahdijual.com/depok/944400-primera-residence-hunian-nyaman-di-jalan-raya-tanah-baru.html       
    778     97    70       http://rumahdijual.com/depok/726495-perumahan-cantik-dekat-kampus-ui.html                               
    778     97    60       http://rumahdijual.com/depok/678776-perumahan-azkana-primera-depok.html                                 
    779     82    51       http://rumahdijual.com/depok/1260309-rumah-indent-dekat-stasiun-dp-angsur-24x.html                      
    780     90    65       http://rumahdijual.com/depok/1016550-rumah-kamar-3-perumahan-puri-asri-tanah-baru.html                  
    780     90    60       http://rumahdijual.com/depok/672801-rumah-ready-di-grand-depok-city-sp-090-acacia.html                  
    780     90    55       http://rumahdijual.com/depok/1206527-rumah-baru-di-acacia-gdc-depok-r21-0425-a.html                     
    780     85    88       http://rumahdijual.com/depok/779494-rumah-di-jual-kelapa-dua-depok-780jt.html                           
    780     85    56       http://rumahdijual.com/depok/1202605-rumah-strategis-bernuansa-relejius-di-daerah-kelapa-dua-depok.html 
    780     84    75       http://rumahdijual.com/depok/413378-townhouse-margo-residen.html                                        
    780     78    36       http://rumahdijual.com/depok/1046742-dijual-cepat-rumah-sangat-strategis-di-kober-jl-margonda.html      
    780     72    70       http://rumahdijual.com/depok/1107834-kemang-swatama-desain-rumah-sesuai-pembeli-0859-6671-7207-a.html   
    780     120   80       http://rumahdijual.com/depok/899879-dijual-rumah-minimalis-di-cinere.html                               
    780     106   60       http://rumahdijual.com/depok/791716-town-house-green-lite-sawangan-depok.html                           
    780     106   60       http://rumahdijual.com/depok/805470-town-house-green-lite-harga-murah-di-sawangan-depok.html            
    780     106   60       http://rumahdijual.com/depok/805582-town-house-harga-murah-meriah-di-sawangan-depok.html                
    780     106   60       http://rumahdijual.com/depok/805670-town-house-green-lite-harga-sangat-terjangkau-di-sawangan.html      
    780     106   60       http://rumahdijual.com/depok/888263-rumah-depok-favorite-lokasi-premium-siap-huni-nyaman.html           
    780     105   80       http://rumahdijual.com/depok/842034-dijual-rumah-tanah-baru-beji-depok.html                             
    780     100   85       http://rumahdijual.com/depok/935656-rumah-minimalis-eksklusif-di-depok-timur-free-kitchen-set.html      
    785     98    70       http://rumahdijual.com/depok/1132558-ayo-buruan-beli-rumah-di-taman-bumi-agung-depok.html               
    785     97    60       http://rumahdijual.com/depok/1293069-rumah-cantik-siap-huni-60-97-kukusan-beji-depok.html               
    785     82    65       http://rumahdijual.com/depok/1131549-perumahan-premiere-depok-nyaman-sangat-strategis.html              
    785     120   80       http://rumahdijual.com/depok/751357-cluster-exclusive-yang-asri-di-kemang-studio-alam-depok.html        
    785     115   60       http://rumahdijual.com/depok/959172-rumah-baru-dalam-kavling-ui-timur-tanah-baru.html                   
    785     115   60       http://rumahdijual.com/depok/986418-azkana-house.html                                                   
    785     104   70       http://rumahdijual.com/depok/871796-rumah-idaman-murah-di-perumahan-exclusive-bella-casa-residence.html 
    785     100   70       http://rumahdijual.com/depok/1042080-ready-stock-rumah-di-taman-bumi-agung-residence-sawangan.html      
    785     100   70       http://rumahdijual.com/depok/585445-taman-bumi-agung-residence.html                                     
    785     100   70       http://rumahdijual.com/depok/1138109-bumi-agung-sawangan-depok.html                                     
    785     100   70       http://rumahdijual.com/depok/1125151-rumah-mewah-paling-murah-di-sawangan.html                          
    786     90    45       http://rumahdijual.com/depok/1266758-depok-perumahan-grand-depok-city-depok.html                        
    789     75    63       http://rumahdijual.com/depok/1151032-town-house-depok-permadani-margonda-residence-500m-dari-jl.html    
    790     90    60       http://rumahdijual.com/depok/1066205-cluster-minimalis-pitara-depok.html                                
    790     84    84       http://rumahdijual.com/depok/629708-duta-town-house-depok-jawa-barat.html                               
    790     72    86       http://rumahdijual.com/depok/893709-rumah-di-perumahan-taman-ventura-beji-depok.html                    
    790     72    72       http://rumahdijual.com/depok/1162042-rumah-cluster-2-lantai-dekat-stasiun-di-beji-depok.html            
    790     72    70       http://rumahdijual.com/depok/1119523-rumah-murah-desain-suka-suka-kemang-swatama-depok-residence.html   
    790     120   56       http://rumahdijual.com/depok/993734-gaharu-residance-sukatani-depok.html                                
    790     120   56       http://rumahdijual.com/depok/963715-rumah-eksklusif-modern-harga-ekonomis.html                          
    790     120   56       http://rumahdijual.com/depok/795982-hunian-tropis-ekonomis-gaharu-residence-depok.html                  
    790     120   56       http://rumahdijual.com/depok/786479-hunian-sehat-serta-ekonomis-di-gaharu-residance-depok.html          
    790     120   56       http://rumahdijual.com/depok/715190-cluster-gaharu-residance-cantik-minimalis-modern-harga-ekonomis.html
    790     120   56       http://rumahdijual.com/depok/1027836-gaharu-residence.html                                              
    790     120   36       http://rumahdijual.com/depok/479093-grand-depok-city-dp-10-juta-cluster-anggrek-2-a.html                
    790     100   80       http://rumahdijual.com/depok/1055191-rumah-2-lantai-di-pitara-depok-dekat-pskd.html                     
    792     109   65       http://rumahdijual.com/depok/1166922-rumah-depok-bebas-biaya-kpr.html                                   
    792     109   65       http://rumahdijual.com/depok/819628-rumah-siap-huni-lokasi-pingir-jalan-raya-tanah-baru.html            
    792     109   65       http://rumahdijual.com/depok/879961-hunian-minimalis-lokasi-strategis-beji-depok.html                   
    793     120   36       http://rumahdijual.com/depok/1190104-new-cluster-anggrek-2ext-dp-cuma-10-juta.html                      
    793     120   36       http://rumahdijual.com/depok/1106865-depok-margonda-raya-jl-kartini-sukmajaya-depok.html                
    793     120   36       http://rumahdijual.com/depok/749451-rumah-dp-10juta-langsung-akad.html                                  
    793     120   36       http://rumahdijual.com/depok/662601-rumah-dijual-anggrek-3-gdc.html                                     
    793     120   36       http://rumahdijual.com/depok/1106852-depok-margonda-raya-jl-kartini-depok.html                          
    793     109   65       http://rumahdijual.com/depok/1227542-azkana-primera-lokasi-terdepan-harga-ringan.html                   
    793     109   65       http://rumahdijual.com/depok/850050-cluster-modern-minimalis-selangkah-jaksel-dan-kampus-ui.html        
    793     109   65       http://rumahdijual.com/depok/945940-azkana-primera-cluster-elit-harga-iriitt.html                       
    793     109   65       http://rumahdijual.com/depok/1194653-new-azkana-primera-residence-hot-promo-free-biaya-kpr.html         
    793     109   65       http://rumahdijual.com/depok/1193024-cluster-azkana-primera-hot-promo-free-biaya-kpr.html               
    793     109   65       http://rumahdijual.com/depok/873234-rumah-minimalis-lokasi-strategis-kota-depok.html                    
    795     98    69       http://rumahdijual.com/depok/413364-depok-perumahan-robina-village-sawangan.html                        
    795     97    60       http://rumahdijual.com/depok/983526-di-jual-rumah-baru-mulus-tanpa-cacat-siap-huni.html                 
    795     78    70       http://rumahdijual.com/depok/1048458-rumah-cluster-murah-dua-lantai-di-cimanggis-depok.html             
    795     78    70       http://rumahdijual.com/depok/1259164-harmony-residen.html                                               
    795     78    70       http://rumahdijual.com/depok/1238767-townhouse-cantik-tanpa-dp-di-cimanggis-depok.html                  
    795     78    70       http://rumahdijual.com/depok/1230951-harmony-residence-cimanggis.html                                   
    795     78    69       http://rumahdijual.com/depok/1135298-rumah-strategis-pinggir-jalan-di-cimanggis-depok.html              
    795     72    69       http://rumahdijual.com/depok/1000974-rumah-murah-di-cimanggis-depok-harmony-residence.html              
    795     70    78       http://rumahdijual.com/depok/1059667-rumah-minimalis-dua-lantai-di-cimanggis-depok.html                 
    795     120   80       http://rumahdijual.com/depok/1268079-di-jual-rumah-siap-huni-tanpa-renovasi-di-kalimulya.html           
    797     94    56       http://rumahdijual.com/depok/822798-hunian-siap-huni-kualitas-terbaik-di-depok.html                     
    798     72    72       http://rumahdijual.com/depok/681730-cluster-cinere.html                                                 
    799     97    60       http://rumahdijual.com/depok/895797-perumahan-primera-residence-depok.html                              
    799     77    72       http://rumahdijual.com/depok/1171702-town-house-mansion-hills-cinere-promo-awal-tahun-akses.html        
    799     117   69       http://rumahdijual.com/depok/959225-rumah-baru-siap-huni-di-tanah-baru-jl-r.html                        
    799     114   68       http://rumahdijual.com/depok/919268-rumah-siap-huni-lokasi-strategis.html                               
    799     114   68       http://rumahdijual.com/depok/898951-rumah-idaman-nyaman-lokasi-depok-terdepan.html                      
    799     114   68       http://rumahdijual.com/depok/1061548-hunian-ciamik-lokasi-strategis-di-tanah-baru-depok.html            
    800     98    65       http://rumahdijual.com/depok/1129916-rumah-minimalis-dijual-cepat-daerah-tanah-baru-depok.html          
    800     98    45       http://rumahdijual.com/depok/1046771-rumah-minimalis-modern-daerah-tanah-baru-depok.html                
    800     96    45       http://rumahdijual.com/depok/919967-di-jual-rumah-cantik-cluster-alpinia-gdc-270-a.html                 
    800     95    60       http://rumahdijual.com/depok/978395-launching-cluster-di-pinggir-jalan-raya-caringin-rangkapan-jaya.html
    800     93    70       http://rumahdijual.com/depok/1294192-rumah-nyaman-strategis-di-kukusan.html                             
    800     93    45       http://rumahdijual.com/depok/1177192-dijual-rumah-siap-huni.html                                        
    800     90    80       http://rumahdijual.com/depok/591212-rumah-di-perumahan-taman-anggrek-cimanggis-depok.html               
    800     90    80       http://rumahdijual.com/depok/1105351-dijual-rumah-murah-dikelapa-dua-depok.html                         
    800     90    65       http://rumahdijual.com/depok/1036397-di-jual-rumah-cantik-siap-huni-di-perumahan-permata.html           
    800     90    50       http://rumahdijual.com/depok/1196716-town-house-rumah-strategis-dan-nyaman-di-margonda-depok.html       
    800     85    75       http://rumahdijual.com/depok/1246220-rumah-dijual-ada-3-unit-dekat-dengan-ui.html                       
    800     80    50       http://rumahdijual.com/depok/915070-rumah-di-puri-ismaya-cinere.html                                    
    800     78    84       http://rumahdijual.com/depok/1248541-cluster-dekat-tol-di-depok.html                                    
    800     77    72       http://rumahdijual.com/depok/798550-rumah-baru-nuasa-mewah-harga-terjangkau-di-sawangan-depok.html      
    800     72    84       http://rumahdijual.com/depok/1110764-cluster-limo-regency-meruyung-dekat-kubah-mas-depok-jawa.html      
    800     72    72       http://rumahdijual.com/depok/1099469-rumah-keren-2-lantai-hanya-3-menit-menuju-statsiun.html            
    800     65    80       http://rumahdijual.com/depok/967382-4-unit-rumah-baru-bisa-kpr-kukusan-depok.html                       
    800     120   69       http://rumahdijual.com/depok/916805-rumah-dijual-di-pondok-petir.html                                   
    800     120   60       http://rumahdijual.com/depok/882170-rumah-baru-dalam-mini-cluster-tanah-baru-depok.html                 
    800     120   24       http://rumahdijual.com/depok/838979-rumah-di-mampang-depok.html                                         
    800     119   45       http://rumahdijual.com/depok/1304872-rumah-aman-bebas-banjir-depok-jawa-barat.html                      
    800     114   75       http://rumahdijual.com/depok/991489-di-jual-rumah-di-villa-pertiwi.html                                 
    800     112   80       http://rumahdijual.com/depok/740543-dijual-rumah-grand-depok-city-cluster-jasmine.html                  
    800     110   80       http://rumahdijual.com/depok/846034-dijual-rumah-strategis-murah-di-kelapa-dua-depok.html               
    800     109   85       http://rumahdijual.com/depok/1095232-di-cinere-lokasi-sangat-strategis.html                             
    800     106   80       http://rumahdijual.com/depok/951646-rumah-bagus-1-5-lt-dijual-beserta-isi-butuh.html                    
    800     105   72       http://rumahdijual.com/depok/776479-di-jual-rumah-cluster-bagus-di-belacassa-depok-160-a.html           
    800     105   71       http://rumahdijual.com/depok/1022330-rumahbaru-jual-murah-dekat-pintu-tol-cijago-bisa-kpr.html          
    800     105   70       http://rumahdijual.com/depok/694961-di-jual-rumah-di-perumahan-bellacasa-depok.html                     
    800     105   54       http://rumahdijual.com/depok/1011512-rumah-murah-minimalis-di-cimanggis-depok-shm.html                  
    800     105   54       http://rumahdijual.com/depok/1065796-dijual-rumah-cluster-lb-lt-54m2-105m2-sukmajaya.html               
    800     105   48       http://rumahdijual.com/depok/1151797-botania-lake-residence.html                                        
    800     104   78       http://rumahdijual.com/depok/1298957-town-house-2-lantai-siap-huni-di-depok-2-a.html                    
    800     104   50       http://rumahdijual.com/depok/1025455-dijual-rumah-mewah-harga-murah.html                                
    800     101   80       http://rumahdijual.com/depok/1026053-rumah-di-grand-depok-city-sp-205-a.html                            
    800     101   80       http://rumahdijual.com/depok/1013062-rumah-siap-huni-di-grand-depok-city.html                           
    800     100   75       http://rumahdijual.com/depok/1098792-rumah-murah-menawan-di-beji-permai.html                            
    800     100   75       http://rumahdijual.com/depok/1096948-rumah-murah-menawan-di-depok.html                                  
    800     100   45       http://rumahdijual.com/depok/1206707-rumah-cantik-strategis-di-tanah-baru.html
    

## House Price Between 800-900 Mio IDR

### Visualize Data


```python
df = visualizeData('depok', 800, 900);
```


![png](png/output_77_0.png)



```python
avg = averageMeasures(df)
```

    
    AVERAGE MEASURES
    -----------------
    
    building    99
        land   127
       price   852
    

### Analyze the Data of House Price Between 800 - 900 Mio IDR


```python
mostSpacious(df)
```

    
    MOST SPACIOUS LAND
    -----------------
    
        bath     2
         bed     3
    building   165
        land   550
       price   800
         url   http://rumahdijual.com/depok/900849-dijual-rumah-kebun-hijau-shm-imb-cagar-alam-depok.html
    
    MOST SPACIOUS BUILDING
    -----------------
    
        bath     3
         bed     3
    building   300
        land   451
       price   825
         url   http://rumahdijual.com/depok/235813-jual-cepat-bu-rumah-lux-dan-6-pintu-kontrakan.html
    


```python
selectEconomical(df, avg, unit)
```

    
    MOST ECONOMICAL
    -----------------
    is when the price is really below average: 852 (million IDR) but you get above the average land: 127 (square meters) and above the average building: 99 (square meters)
    
    You are blessed to choose one of these 71  houses:
    
    price  land building                                                                                                  url
    800     550   165      http://rumahdijual.com/depok/900849-dijual-rumah-kebun-hijau-shm-imb-cagar-alam-depok.html        
    800     550   120      http://rumahdijual.com/depok/907483-rumah-suasana-villa-pedesaan.html                             
    800     396   112      http://rumahdijual.com/depok/1097593-rumah-kebayunan-tapos-depok.html                             
    800     316   200      http://rumahdijual.com/depok/1027682-1-rumah-tinggal-beserta-5-pintu-kontrakan.html               
    800     220   220      http://rumahdijual.com/depok/914554-dijual-rumah-di-sawangan-depok.html                           
    800     220   100      http://rumahdijual.com/depok/864729-rumah-minimalis-siap-huni-asri-murah-di-cinangka-sawangan.html
    800     207   150      http://rumahdijual.com/depok/1283761-rumah-murah-masuk-mobil-di-depok-r21-0477-a.html             
    800     207   150      http://rumahdijual.com/depok/1069233-rumah-cluster-207m2-strategis-depok.html                     
    800     207   130      http://rumahdijual.com/depok/1073540-rumah-mewah-harga-sederhana-dekat-jalan-raya-depok-rute.html 
    800     205   120      http://rumahdijual.com/depok/1158141-rumah-second-siap-huni-murah-di-depok.html                   
    800     205   100      http://rumahdijual.com/depok/908110-rumah-second-minimalis-siap-huni-di-kelapa-2-depok.html       
    800     199   160      http://rumahdijual.com/depok/1258118-rumah-luas-nyaman-dekat-matoa-golf-tanah-baru-ada.html       
    800     195   157      http://rumahdijual.com/depok/1035757-rumah-murah-dan-strategis-pondok-cina-depok.html             
    800     190   170      http://rumahdijual.com/depok/1065094-jual-cepat-rumah-di-depok.html                               
    800     185   130      http://rumahdijual.com/depok/1212455-dijual-rumah-second-bu.html                                  
    800     182   130      http://rumahdijual.com/depok/1185312-dijual-cepat-rumah-second-pancoran-mas-depok.html            
    800     179   140      http://rumahdijual.com/depok/1194047-rumah-luas-dan-strategis-di-depok-timur.html                 
    800     176   150      http://rumahdijual.com/depok/853730-rumah-murah-tanah-ngantong-luas-pekapuran-depok.html          
    800     175   105      http://rumahdijual.com/depok/1193953-dijual-rumah-di-margonda-depok-cocok-untuk-rumah-kos.html    
    800     171   145      http://rumahdijual.com/depok/1119458-hunian-asri-dan-nyaman-di-pinggir-kota.html                  
    800     170   150      http://rumahdijual.com/depok/903688-rumah-dijual-cepat.html                                       
    800     167   150      http://rumahdijual.com/depok/900594-dijual-rumah-kios-siap-huni-hanya-3-menit-ke.html             
    800     155   125      http://rumahdijual.com/depok/1268588-rumah-strategis-investasi-cerdas-masa-depan-di-sawangan.html 
    800     154   100      http://rumahdijual.com/depok/1145096-rumah-dijual-depok-murah-pancoran-mas.html                   
    800     154   100      http://rumahdijual.com/depok/1179110-rumah-dijual-depok-baru-maharaja-2016-a.html                 
    800     150   120      http://rumahdijual.com/depok/904257-rumah-pinggir-jalan-di-beji-depok.html                        
    800     150   100      http://rumahdijual.com/depok/1050020-rumah-di-tengsh-komplek.html                                 
    800     137   137      http://rumahdijual.com/depok/899981-rumah-di-jual-di-villa-pertiwi.html                           
    810     190   130      http://rumahdijual.com/depok/1089923-rumah-dijual-di-depok-utara.html                             
    810     150   120      http://rumahdijual.com/depok/1264216-rumah-mewah-2-lantai-di-cimanggis.html                       
    815     500   200      http://rumahdijual.com/depok/995110-rumah-htung-tanah-pinggir-jalan-bonus-3-phon-mngga.html       
    815     280   250      http://rumahdijual.com/depok/796949-rumah-dan-3-kontrakan-di-cilodong-depok-280m2-bagus.html      
    817     179   140      http://rumahdijual.com/depok/1034250-rumah-dalam-kompleks-murah-depok-timur-bu.html               
    825     451   300      http://rumahdijual.com/depok/235813-jual-cepat-bu-rumah-lux-dan-6-pintu-kontrakan.html            
    825     156   100      http://rumahdijual.com/depok/702516-baru-type-100-dgn-design-minimalis-modern-di-pondok.html      
    835     500   200      http://rumahdijual.com/depok/190139-rumah-besar-dan-halaman-luas-depok.html                       
    835     170   100      http://rumahdijual.com/depok/748219-rumah-murah-tanah-luas-banget-170m2-4-kamar-7-a.html          
    850     386   150      http://rumahdijual.com/depok/1226189-dijual-rumah-besar-harga-standar-di-beji-depok.html          
    850     365   100      http://rumahdijual.com/depok/862654-rumah-muraahh-di-depok-cimanggis.html                         
    850     260   240      http://rumahdijual.com/depok/1074539-rumah-besar-jual-cepat-lt-260-lb-240-a.html                  
    850     210   180      http://rumahdijual.com/depok/1174494-dijual-rumah-hoek-di-pondok-sukatani-permai-tapos-depok.html 
    850     207   150      http://rumahdijual.com/depok/1062946-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html     
    850     207   150      http://rumahdijual.com/depok/1061871-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html     
    850     207   130      http://rumahdijual.com/depok/1064989-rumah-luas-dekat-jalan-raya-dan-lantai-full-granite.html     
    850     207   130      http://rumahdijual.com/depok/1160758-rumah-ngantong-strategis-di-pitara-depok.html                
    850     207   130      http://rumahdijual.com/depok/1139901-rumah-luas-full-granit-banyak-bonusnya.html                  
    850     207   130      http://rumahdijual.com/depok/1139894-rumah-luas-full-granit-banyak-bonusnya.html                  
    850     207   130      http://rumahdijual.com/depok/1139899-rumah-luas-full-granit-banyak-bonusnya.html                  
    850     207   130      http://rumahdijual.com/depok/1139896-rumah-luas-full-granit-banyak-bonusnya.html                  
    850     207   130      http://rumahdijual.com/depok/1101559-hunian-luas-dekat-jalan-raya.html                            
    850     207   130      http://rumahdijual.com/depok/1213258-rumah-minimalis-dengan-tanah-luas.html                       
    850     207   130      http://rumahdijual.com/depok/1060442-rumah-siap-huni-pitara-depok.html                            
    850     207   130      http://rumahdijual.com/depok/1060279-rumah-murah-207m2-depok.html                                 
    850     207   130      http://rumahdijual.com/depok/1059838-rumah-luas-207m2-siap-huni.html                              
    850     207   130      http://rumahdijual.com/depok/1215735-rumah-dengan-tanah-luas-dan-4-kamar-tidur.html               
    850     200   200      http://rumahdijual.com/depok/737579-rumah-cantik-di-parung-serab-depok.html                       
    850     200   150      http://rumahdijual.com/depok/1191631-rumah-idaman-keluarga-besar-dan-bahagia.html                 
    850     200   150      http://rumahdijual.com/depok/1191643-rumah-baru-kuat-dan-manis-impian-anda-semua.html             
    850     200   100      http://rumahdijual.com/depok/1010551-rumah-cilodong-tipe-minimalist-luas-dan-asri.html            
    850     180   100      http://rumahdijual.com/depok/1299528-rumah-asri-di-cinere.html                                    
    850     170   165      http://rumahdijual.com/depok/1001718-dijual-rumah-cinere.html                                     
    850     170   150      http://rumahdijual.com/depok/1111659-rumah-tingkat-di-tanah-baru-depok.html                       
    850     157   100      http://rumahdijual.com/depok/1291935-rumah-di-jual-cepat-850-juta.html                            
    850     155   125      http://rumahdijual.com/depok/1269638-rumah-strategis-pinggir-jalan-raya-muchtar-sawangan.html     
    850     155   120      http://rumahdijual.com/depok/1152950-rumah-baru-bisa-kpr-harga-murah-masih-bisa-nego.html         
    850     152   152      http://rumahdijual.com/depok/1199386-jual-rumah-di-perumahan-tirtamandala-depok.html              
    850     150   140      http://rumahdijual.com/depok/47883-jual-ruman-nyaman-dan-asri-murah-di-meruyung-limo.html         
    850     150   100      http://rumahdijual.com/depok/608960-rumah-minimalis-cluster-griya-pesona-alam.html                
    850     147   150      http://rumahdijual.com/depok/847353-rumah-di-telaga-golf-sawangan-depok.html                      
    850     138   108      http://rumahdijual.com/depok/1171648-rumah-dijual-berikut-perabotan-lengkap-kelapa-dua-depok.html 
    850     128   120      http://rumahdijual.com/depok/806403-dijual-rumah-exclusive-di-beji-depok.html
    


```python
selectModerate(df, avg, unit)
```

    
    MODERATE PRICE
    -----------------
    is when the price is above average: 852 (million IDR) with above-average land: 127 (square meters) and above-average building: 99 (square meters)
    
    
    There are : 103  items with above-average price and above-average land.
    
    There are : 82  items with above-average price, above-average land and above-average building.
    
    price  land building                                                                                                         url
    854     176   120      http://rumahdijual.com/depok/1003349-38-di-jual-rumah-bagus-pondok-duta-1-depok.html                     
    860     160   150      http://rumahdijual.com/depok/594083-rumah-2-lt-murah-di-depok.html                                       
    870     220   200      http://rumahdijual.com/depok/1111360-rumah-di-cimanggis.html                                             
    875     372   168      http://rumahdijual.com/depok/1276230-rumah-murah-di-belakang-taman-anyelir-gdc.html                      
    875     215   200      http://rumahdijual.com/depok/437506-rumah-cantik-di-cilodong-dekat-gdc-r21-0044-a.html                   
    875     200   180      http://rumahdijual.com/depok/877266-rumah-komplek-sukmajaya.html                                         
    875     190   160      http://rumahdijual.com/depok/700656-rumah-eks-orang-bali.html                                            
    875     151   187      http://rumahdijual.com/depok/673582-rumh-dkt-stasiun-dpk-baru-naik-kereta-nglenyer-shm.html              
    875     150   144      http://rumahdijual.com/depok/649365-dijual-rumah-murah-kontrakan-3-petak-di-jl-h.html                    
    875     136   110      http://rumahdijual.com/depok/802461-perumahan-villa-pertiwi-rumah-di-hook-memukau-harga-terjangkau.html  
    880     173   120      http://rumahdijual.com/depok/1037557-127-di-jual-rumah-cantik-2-lantai-raden-saleh.html                  
    880     140   110      http://rumahdijual.com/depok/546483-rumah-di-perum-pelni-juanda-depok-dekat-dengan-tol.html              
    888     136   100      http://rumahdijual.com/depok/1004275-rumah-murah-dan-strategis-didepok.html                              
    890     165   140      http://rumahdijual.com/depok/1276565-rumah-posisi-sudut-jarang-ada-pondok-mekarsari-permai-cimanggis.html
    890     133   100      http://rumahdijual.com/depok/984686-rumah-dijual-cepat.html                                              
    895     176   146      http://rumahdijual.com/depok/986425-pondok-duta-cimanggis-depok.html                                     
    900     372   160      http://rumahdijual.com/depok/934393-rumah-asri-dan-nyaman-di-kalimulya-depok.html                        
    900     350   180      http://rumahdijual.com/depok/1053154-rumah-daerah-cinere.html                                            
    900     350   110      http://rumahdijual.com/depok/896163-rumah-murah-banget-di-cakra-cinere-depok.html                        
    900     337   200      http://rumahdijual.com/depok/872327-rumah-luas-harga-puas-di-depok.html                                  
    900     337   200      http://rumahdijual.com/depok/813912-rumah-di-cimanggis-depok.html                                        
    900     328   150      http://rumahdijual.com/depok/957483-rumah-lama-luas-328m-di-jl-rtm-kelapa-dua.html                       
    900     310   150      http://rumahdijual.com/depok/799968-rumah-second-beserta-kontrakan.html                                  
    900     300   200      http://rumahdijual.com/depok/1215572-rumah-sederhana-di-pancoran-mas-depok.html                          
    900     222   110      http://rumahdijual.com/depok/1249549-rumah-daerah-cibinong-plus-2-rumah-kontrakan-di-jalan.html          
    900     213   140      http://rumahdijual.com/depok/1103713-dijual-rumah-di-beji-depok.html                                     
    900     207   150      http://rumahdijual.com/depok/1114413-rumah-luas-150-207-ready-harga-murah.html                           
    900     207   150      http://rumahdijual.com/depok/1087893-rumah-luas-type-150-207-pitara-depok.html                           
    900     207   150      http://rumahdijual.com/depok/1056912-rumah-luas-type-150-207-siap-huni.html                              
    900     207   150      http://rumahdijual.com/depok/1101162-rumah-mewah-banyak-grratis-nya.html                                 
    900     207   150      http://rumahdijual.com/depok/1115673-rumah-cluster-fuul-bonus.html                                       
    900     207   150      http://rumahdijual.com/depok/1064651-cluster-mewah-harga-murah-kota-depok.html                           
    900     207   150      http://rumahdijual.com/depok/1184031-hanya-1-unit-type-207-meter-banyak-bonus-nya.html                   
    900     207   130      http://rumahdijual.com/depok/1115564-rumah-luas-full-granit-banyak-bonusnya.html                         
    900     207   130      http://rumahdijual.com/depok/1185969-rumah-cluster-depok-pitara-raya.html                                
    900     207   130      http://rumahdijual.com/depok/1133838-rumah-luas-full-granit-banyak-bonusnya.html                         
    900     207   130      http://rumahdijual.com/depok/1115602-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html            
    900     207   130      http://rumahdijual.com/depok/1118231-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html            
    900     207   130      http://rumahdijual.com/depok/1118567-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html            
    900     207   130      http://rumahdijual.com/depok/1115740-promo-tutup-tahun.html                                              
    900     207   130      http://rumahdijual.com/depok/1115763-rumah-luas-dekat-jalan-raya-di-pitara.html                          
    900     207   130      http://rumahdijual.com/depok/1118617-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html            
    900     207   130      http://rumahdijual.com/depok/1074081-rumah-mewah-harga-murah-depok.html                                  
    900     207   130      http://rumahdijual.com/depok/1074141-rumah-cluster-lt-207-harga-nego-keras-depoo.html                    
    900     207   130      http://rumahdijual.com/depok/1133844-rumah-luas-full-granit-banyak-bonusnya.html                         
    900     207   130      http://rumahdijual.com/depok/1118564-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html            
    900     207   130      http://rumahdijual.com/depok/1118561-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html            
    900     207   130      http://rumahdijual.com/depok/1118235-hunian-luas-banyak-bonus-di-jalan-pitara-raya.html                  
    900     207   130      http://rumahdijual.com/depok/1118241-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html            
    900     207   130      http://rumahdijual.com/depok/1118228-promo-tutup-tahun.html                                              
    900     207   130      http://rumahdijual.com/depok/1118220-rumah-luas-dekat-jalan-raya-di-pitara.html                          
    900     207   130      http://rumahdijual.com/depok/1118213-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html            
    900     207   130      http://rumahdijual.com/depok/1118200-promo-tutup-tahun.html                                              
    900     207   130      http://rumahdijual.com/depok/1118196-rumah-luas-dekat-jalan-raya-di-pitara.html                          
    900     207   130      http://rumahdijual.com/depok/1115759-rumah-luas-dekat-jalan-raya-di-pitara.html                          
    900     207   130      http://rumahdijual.com/depok/1118557-promo-tutup-tahun.html                                              
    900     207   130      http://rumahdijual.com/depok/1182818-tahap-pembangunan-rumah-luas-di-pitara-depok.html                   
    900     207   130      http://rumahdijual.com/depok/1117817-rumah-non-kpr.html                                                  
    900     207   130      http://rumahdijual.com/depok/1182803-rumah-pitara-tanah-luas-bangunan-memuaskan.html                     
    900     200   190      http://rumahdijual.com/depok/549506-rumah-asri-di-cinangka-depok.html                                    
    900     193   110      http://rumahdijual.com/depok/1062883-rumah-di-lokasi-strategis-cimanggis-depok.html                      
    900     188   180      http://rumahdijual.com/depok/1178319-rumah-dijual-cilondong-900jt.html                                   
    900     185   145      http://rumahdijual.com/depok/1149207-jual-rumah-komplek-pelni-depok-harga-di-bawah-pasaran.html          
    900     182   230      http://rumahdijual.com/depok/805755-rumah-lt-182-lb-230-di-villa-pertiwi-depok.html                      
    900     180   170      http://rumahdijual.com/depok/1029836-rumah-asri-bernuansa-bali-di-permata-depok-jual-cepat.html          
    900     180   120      http://rumahdijual.com/depok/1160809-dijual-rumah-pinggir-jalan-raya.html                                
    900     165   100      http://rumahdijual.com/depok/1268862-dijual-rumah-cantik-2-lantai-cluster-taman-ayun-sawangan.html       
    900     156   240      http://rumahdijual.com/depok/950742-komp-marinir-dekat-kubah-mas-limo-depok.html                         
    900     150   150      http://rumahdijual.com/depok/1125314-rumah-besar-harga-kecil.html                                        
    900     150   120      http://rumahdijual.com/depok/709158-dijual-rumah-nuansa-asri-bebas-banjir-akses-mudah-lt.html            
    900     150   102      http://rumahdijual.com/depok/1136694-depok-rumah-asri-kondisi-baru-bagus-jarang-ada.html                 
    900     150   102      http://rumahdijual.com/depok/1129214-depok-rumah-asri-kondisi-bagus-jarang-ada.html                      
    900     150   100      http://rumahdijual.com/depok/1301697-rumah-2-lantai-di-rawa-geni.html                                    
    900     150   100      http://rumahdijual.com/depok/609072-rumah-minimalis-cluster-10-menit-stasiun-depok-lama.html             
    900     143   110      http://rumahdijual.com/depok/534762-dijual-rumah-exclusive-di-pusat-kota-depok.html                      
    900     140   200      http://rumahdijual.com/depok/380138-dijual-cepat-rumah-didaerah-depok.html                               
    900     140   120      http://rumahdijual.com/depok/1229721-rumah-di-komplek-puribali-bojongsari-depok.html                     
    900     139   160      http://rumahdijual.com/depok/787016-perumahan-depok-maharaja.html                                        
    900     135   135      http://rumahdijual.com/depok/1235748-dijual-rumah-strategis-pinggir-jalan-di-beji-depok-pr1040.html      
    900     135   117      http://rumahdijual.com/depok/1226415-rumah-strategis-di-komplek-pelni-kota-depok.html                    
    900     134   180      http://rumahdijual.com/depok/1257157-rumah-dijual-murah-daerah-tole-iskandar-depok-perumahan-nyaman.html 
    900     130   100      http://rumahdijual.com/depok/1174545-rumah-siap-huni-lingkungan-asri.html
    


```python
selectExpensive(df, avg, unit)
```

    
    EXPENSIVE PRICE
    -----------------
    is when the price is above average: 852 (million IDR) but you only get land below average: 127 (square meters) and building below average: 99 (square meters).
    
    
    
    There are : 118  items that matched the EXPENSIVE category.
    
    price  land building                                                                                                         url
    855     90    75       http://rumahdijual.com/depok/1119092-rumah-2-lantai-harga-800-jutaan.html                                
    855     120   80       http://rumahdijual.com/depok/1061963-rumah-siap-huni-di-gdc-sp-183-a.html                                
    855     109   69       http://rumahdijual.com/depok/248997-rumah-nyaman-robina-village-sawangan-depok.html                      
    856     126   56       http://rumahdijual.com/depok/1280600-cluster-minimalis-lokasi-nempel-kampus-ui.html                      
    856     126   56       http://rumahdijual.com/depok/1279974-hunian-ciamik-nan-exclusive-di-beji-tanah-baru.html                 
    857     101   61       http://rumahdijual.com/depok/799662-rumah-murah-ready-stock-di-selatan-jakarta.html                      
    857     101   61       http://rumahdijual.com/depok/810409-rumah-murah-bebas-banjir.html                                        
    858     120   45       http://rumahdijual.com/depok/1080541-rumah-minimalis-lokasi-strategis-harga-menarik.html                 
    860     84    72       http://rumahdijual.com/depok/821387-rumah-2-lantai-jalan-pendowo-daerah-limo-cinere-siap.html            
    860     120   45       http://rumahdijual.com/depok/929681-grand-depok-city-10-juta-langsung-akad.html                          
    860     120   45       http://rumahdijual.com/depok/775905-rumah-minimalis-dalam-cluster-keamanan-24jam-bebas-banjir.html       
    863     120   60       http://rumahdijual.com/depok/1040473-rumah-minimalis-cluster-dp-bebas-free-biaya2-di-cilangkap.html      
    864     84    45       http://rumahdijual.com/depok/1272755-royal-matoa-krukut-cinere-800jutaan.html                            
    867     75    80       http://rumahdijual.com/depok/1189327-rumah-town-house-dekat-stasiun-depok.html                           
    867     109   72       http://rumahdijual.com/depok/1019441-rumah-mewah-di-lokasi-strategis-lingkunagn-nyaman-dan-asri.html     
    870     98    70       http://rumahdijual.com/depok/983114-rumah-mewah-bebas-biaya-surat-siap-huni-di-pinggir.html              
    870     97    70       http://rumahdijual.com/depok/865096-rumah-ekslusive-2-lantai-strtaegis-bumi-agung-residence-sawangan.html
    870     90    65       http://rumahdijual.com/depok/885117-rumah-tanah-baru-depok.html                                          
    870     75    70       http://rumahdijual.com/depok/808032-rumah-murah-di-cibubur-samping-raffles-hill.html                     
    870     105   54       http://rumahdijual.com/depok/937168-di-jual-rumah-bagus-siap-huni-permata-depok-regency.html             
    874     81    90       http://rumahdijual.com/depok/874605-cluster-minimalis-2-lt-lokasi-strategis-di-kelapa-2-a.html           
    874     81    90       http://rumahdijual.com/depok/902501-di-jual-rumah-baru-cluster-strategis-dan-nyaman-di.html              
    874     81    90       http://rumahdijual.com/depok/865755-permata-kelapa-dua-cimanggis-depok.html                              
    874     120   70       http://rumahdijual.com/depok/1219940-rumah-baru-2-lantai-harga-1-lantai-di-sarua.html                    
    874     120   70       http://rumahdijual.com/depok/1303841-rumah-baru-2-lantai-harga-ringan-di-new-estesia.html                
    874     120   70       http://rumahdijual.com/depok/1262702-cluster-new-estesia-residence-serua.html                            
    875     96    53       http://rumahdijual.com/depok/1267137-citralake-sawangan-ciputra.html                                     
    875     90    65       http://rumahdijual.com/depok/807732-di-jual-rumah-bagus-siap-huni-depok-timur-188-a.html                 
    875     89    90       http://rumahdijual.com/depok/904376-cluster-strategis-dan-nyaman-di-kelapa-dua-depok.html                
    875     84    90       http://rumahdijual.com/depok/894533-rumah-townhouse-2lantai-kelapa-dua-depok-800jtan.html                
    875     81    90       http://rumahdijual.com/depok/793162-cluster-permata-kelapa-dua.html                                      
    875     81    90       http://rumahdijual.com/depok/906242-cluster-strategis-di-depok-dalam-lokasi-yang-dicari-banyak.html      
    875     81    90       http://rumahdijual.com/depok/891636-cluster-permata-kelapa-dua.html                                      
    875     81    90       http://rumahdijual.com/depok/939444-terbatas-cluster-mewah-harga-murah-dan-strategis-depok-dijamin.html  
    875     81    90       http://rumahdijual.com/depok/910832-rumah-murah-dan-nyaman-didepok.html                                  
    875     81    90       http://rumahdijual.com/depok/905955-dijual-rumah-cluster-2-lantai-murah-di-kelapa-dua.html               
    875     81    90       http://rumahdijual.com/depok/906012-cluster-strategis-dan-nyaman-di-kelapa-dua-depok.html                
    875     81    90       http://rumahdijual.com/depok/1017753-rumah-dijual-di-kelapa-dua-depok-2-lantai-murah.html                
    875     81    90       http://rumahdijual.com/depok/902624-rumah-cluster-strategis-dan-nyaman-di-kelapa-dua-depok.html          
    875     81    90       http://rumahdijual.com/depok/971045-rumah-dijual-di-depok-dijual-rumah-di-depok-cluster.html             
    875     62    75       http://rumahdijual.com/depok/1286521-rumah-ready-stock-di-kukusan-beji.html                              
    875     122   90       http://rumahdijual.com/depok/1022717-di-jual-rumah-cuakep-siap-huni-tanpa-renovasi-di.html               
    875     110   90       http://rumahdijual.com/depok/780853-rumah-baru-dibangun-perum-pelni-depok.html                           
    875     109   72       http://rumahdijual.com/depok/638920-rumah-tingkat-cluster-eclusive-jalan-kaki-ke-ui-shm.html             
    875     107   70       http://rumahdijual.com/depok/959211-japat-residence-kelapa-dua-depok-rumah-min.html                      
    875     107   70       http://rumahdijual.com/depok/1164259-rumah-strategis-siap-huni-kelapa-dua-depok.html                     
    875     105   80       http://rumahdijual.com/depok/1049110-griya-sawo-siap-huni-murah.html                                     
    875     10    70       http://rumahdijual.com/depok/1295137-rumah-minimalis-di-kelapa-dua.html                                  
    876     84    78       http://rumahdijual.com/depok/1027615-perumahan-bungur-residence-cimanggis-depok.html                     
    876     78    84       http://rumahdijual.com/depok/1248548-cluster-dekat-tol-di-depok-1-a.html                                 
    876     78    84       http://rumahdijual.com/depok/1161077-rumah-murah-tanpa-dp-di-cimanggis-depok.html                        
    876     78    84       http://rumahdijual.com/depok/969813-rumah-murah-tanpa-dp-di-cimanggis-depok.html                         
    876     78    84       http://rumahdijual.com/depok/958137-rumah-murah-tanpa-dp-di-cimanggis.html                               
    876     78    84       http://rumahdijual.com/depok/954899-ruman-cantik-minimalis-dekat-tol-cijago.html                         
    876     78    84       http://rumahdijual.com/depok/954639-rumah-cantik-strategis-di-perumahan-bungur-residence.html            
    876     78    84       http://rumahdijual.com/depok/963619-rumah-murah-shm-di-cimanggis-depok.html                              
    876     78    84       http://rumahdijual.com/depok/1246239-rumah-dijual-rumah-murah-tanpa-dp-di-cimanggis-depok.html           
    876     78    84       http://rumahdijual.com/depok/1057246-bungur-residence-rumah-mewah-bisa-kpr-tanpa-dp-dp.html              
    876     78    84       http://rumahdijual.com/depok/1248558-cluster-dekat-tol-di-depok.html                                     
    880     72    85       http://rumahdijual.com/depok/906738-rumah-minimalis-tanah-baru-depok.html                                
    880     100   70       http://rumahdijual.com/depok/955027-taman-bumi-agung-residence-sawangan-depok.html                       
    880     100   70       http://rumahdijual.com/depok/983052-rumah-ready-stock-2-lantai-eksklusif-di-pinggir-jalan.html           
    883     87    70       http://rumahdijual.com/depok/1100837-jasmin-hill-rumah-2-lantai-dp-30-juta-bebas.html                    
    883     87    70       http://rumahdijual.com/depok/1156147-jasmin-hills-sawangan-depok.html                                    
    883     83    70       http://rumahdijual.com/depok/1101956-jasmin-hill-rumah-2-lantai-di-sawangan-dp-irit.html                 
    889     97    88       http://rumahdijual.com/depok/947920-di-jual-rumah-cantik-siap-huni-town-house-cilodong.html              
    889     84    92       http://rumahdijual.com/depok/1254309-rumah-dijual-baru-murah-dan-strategis-di-palomino-residence.html    
    890     92    70       http://rumahdijual.com/depok/1292229-rumah-dijual-rumah-bernuansa-islami-di-kawasan-kubah-mas.html       
    890     120   80       http://rumahdijual.com/depok/1017855-rumah-2-lantai-800-jutaan-di-sawangan.html                          
    890     120   69       http://rumahdijual.com/depok/1016739-di-jual-rumah-baru-di-kalimulya-town-house-grand.html               
    890     120   69       http://rumahdijual.com/depok/494898-dipasarkan-rumah-baru-modern-tropic-akasia-terrace-pondok-petir.html 
    890     120   45       http://rumahdijual.com/depok/1052998-rumah-minimalis-dp-ekonomis-di-pusat-depok.html                     
    890     103   48       http://rumahdijual.com/depok/954775-rumah-dijual-di-kav-pupuk-kujang-depok-1-a.html                      
    890     100   67       http://rumahdijual.com/depok/799626-rumah-1-lantai-ready-stock-di-depok-2015-a.html                      
    894     81    90       http://rumahdijual.com/depok/913021-cluster-minimalis-2-lantai-di-belakang-kampus-gunadarma.html         
    895     90    72       http://rumahdijual.com/depok/863573-rumah-di-cimanggis-depok-puri-khasanah.html                          
    895     84    85       http://rumahdijual.com/depok/1243684-depok-mampang-sawangan-rumah-tingkat-cluster-mewah-dan-murah.html   
    895     84    85       http://rumahdijual.com/depok/1213666-depok-mampang-sawangan-rumah-cluster-tingkat-mewah-siap-huni.html   
    895     84    85       http://rumahdijual.com/depok/1275214-rumah-cluster-tingkat-mewah-jalan-2-mobil.html                      
    895     81    90       http://rumahdijual.com/depok/1024000-cluster-strategis-dan-nyaman-bonus-ac-kelapa-dua-depok.html         
    895     81    90       http://rumahdijual.com/depok/912229-perumahan-murah-di-kelapa-dua-depok.html                             
    895     81    90       http://rumahdijual.com/depok/912694-rumah-dijual-murah-dikelapa-dua-depok.html                           
    895     81    90       http://rumahdijual.com/depok/1012404-hunian-nyaman-di-kelapa-dua-depok.html                              
    895     120   80       http://rumahdijual.com/depok/993155-rumah-hooks-di-komplek-120-meter-tanah-baru-depok.html               
    895     120   55       http://rumahdijual.com/depok/1293018-rumah-cantik-siap-huni-55-120-anggrek-2-grand.html                  
    895     113   80       http://rumahdijual.com/depok/877684-rumah-kelapa-2-depok.html                                            
    897     86    78       http://rumahdijual.com/depok/1230097-rumah-bagus-di-depok.html                                           
    897     86    78       http://rumahdijual.com/depok/816628-town-house-ready-stock-sekitar-cinere-daerah-limo-depok.html         
    897     86    78       http://rumahdijual.com/depok/531435-rumah-ready-stock-cinere-type-78-86m-limo-depok.html                 
    897     84    45       http://rumahdijual.com/depok/1310669-dijual-cluster-murah-diperumahan-mewah-free-ac-tiap-kamar.html      
    900     98    91       http://rumahdijual.com/depok/1047914-limo-cinere-tol-exit.html                                           
    900     90    90       http://rumahdijual.com/depok/1048438-rumah-di-kavling-dekat-perumahan-wisma-mas-cinangka-depok.html      
    900     90    80       http://rumahdijual.com/depok/931368-perumahan-minimalis-pondok-kampoeng-residence-tanah-baru.html        
    900     90    75       http://rumahdijual.com/depok/1039954-luxury-home-your-luxurios-living.html                               
    900     90    70       http://rumahdijual.com/depok/1174035-jasmin-hills-rumah-2-lantai-di-sawangan-depok.html                  
    900     84    85       http://rumahdijual.com/depok/1222567-hunian-strategis-di-kota-depok.html                                 
    900     72    69       http://rumahdijual.com/depok/326951-perumahan-cluster-origin-residences-di-gandul-cinere.html            
    900     2     90       http://rumahdijual.com/depok/923871-panoramic-garden-depok.html                                          
    900     124   60       http://rumahdijual.com/depok/912190-jual-cepat-rumah-di-pinggir-jalan-grand-depok-city.html              
    900     120   90       http://rumahdijual.com/depok/1219356-rumah-depok-beji-dekat-pusat-kota-depok-jalan-masuk.html            
    900     120   90       http://rumahdijual.com/depok/1299692-depok-beji-rumah-dekat-pusat-kota-3-kamar-tidur.html                
    900     120   90       http://rumahdijual.com/depok/1275181-rumah-di-depok-1-jalan-bisa-2-mobil-bisa.html                       
    900     120   72       http://rumahdijual.com/depok/1240740-jual-rumah-cluster-akasia-t-72-120-cendana-regency.html             
    900     120   72       http://rumahdijual.com/depok/1226439-cendana-regency-sawangan-depok.html                                 
    900     120   72       http://rumahdijual.com/depok/1269861-cendana-regency-sawangan-type-72-120-good-investment.html           
    900     120   72       http://rumahdijual.com/depok/1265818-rumah-strategis-dan-nyaman-di-sawangan.html                         
    900     119   70       http://rumahdijual.com/depok/1266065-dijual-bu-rumah-bagus-perumahan-depok-maharaja.html                 
    900     118   80       http://rumahdijual.com/depok/1149273-dijual-rumah-di-depok-cimanggis.html                                
    900     117   78       http://rumahdijual.com/depok/1007673-dijual-rumah-di-lokasi-idaman-keluarga.html                         
    900     115   69       http://rumahdijual.com/depok/1285638-dijual-rumah-2-lantai-ready-stock-di-akasia-terrace.html            
    900     112   90       http://rumahdijual.com/depok/975966-rumah-nyaman-asri-dan-halaman-luas-cinere.html                       
    900     112   90       http://rumahdijual.com/depok/959006-rumah-murah-dijual-di-cinere.html                                    
    900     108   60       http://rumahdijual.com/depok/1265905-rumah-di-jual-daerah-depok.html                                     
    900     105   90       http://rumahdijual.com/depok/1216554-dijual-rumah-jl-boulevard-depok-rk-829-a.html                       
    900     105   90       http://rumahdijual.com/depok/1212914-rumah-keluarga-murah-di-selatan-jakarta-grand-depok-city.html       
    900     104   50       http://rumahdijual.com/depok/170273-banjaran-village.html                                                
    900     101   90       http://rumahdijual.com/depok/894935-hunian-asri-dan-exclusive-di-pusat-kota-depok-ready.html             
    900     100   80       http://rumahdijual.com/depok/998052-jual-butuh-rumah-sangat-strategis-di-depokdekat-stasiun-kereta.html
    

## House Price Between 900 - 1000 Mio IDR

### Visualize Data


```python
df = visualizeData('depok', 900, 1000);
```


![png](png/output_86_0.png)


### Analyze the Data of House Price Between 900 - 1000 mio IDR


```python
avg = averageMeasures(df)
```

    
    AVERAGE MEASURES
    -----------------
    
    building   119
        land   145
       price   946
    


```python
mostSpacious(df)
```

    
    MOST SPACIOUS LAND
    -----------------
    
        bath     3
         bed     3
    building   192
        land   620
       price   970
         url   http://rumahdijual.com/depok/831529-dijual-rumah-di-kawasan-duren-mekar-kecamatan-bojong-sari.html
    
    MOST SPACIOUS BUILDING
    -----------------
    
        bath     4
         bed     4
    building   300
        land   171
       price  1000
         url   http://rumahdijual.com/depok/1024275-rumah-hoek-di-di-komplek-mekarsari-harpan-2-bisa.html
    


```python
selectEconomical(df, avg, unit)
```

    
    MOST ECONOMICAL
    -----------------
    is when the price is really below average: 946 (million IDR) but you get above the average land: 145 (square meters) and above the average building: 119 (square meters)
    
    You are blessed to choose one of these 52  houses:
    
    price  land building                                                                                                 url
    900     372   160      http://rumahdijual.com/depok/934393-rumah-asri-dan-nyaman-di-kalimulya-depok.html                
    900     350   180      http://rumahdijual.com/depok/1053154-rumah-daerah-cinere.html                                    
    900     337   200      http://rumahdijual.com/depok/872327-rumah-luas-harga-puas-di-depok.html                          
    900     337   200      http://rumahdijual.com/depok/813912-rumah-di-cimanggis-depok.html                                
    900     328   150      http://rumahdijual.com/depok/957483-rumah-lama-luas-328m-di-jl-rtm-kelapa-dua.html               
    900     310   150      http://rumahdijual.com/depok/799968-rumah-second-beserta-kontrakan.html                          
    900     300   200      http://rumahdijual.com/depok/1215572-rumah-sederhana-di-pancoran-mas-depok.html                  
    900     213   140      http://rumahdijual.com/depok/1103713-dijual-rumah-di-beji-depok.html                             
    900     207   150      http://rumahdijual.com/depok/1114413-rumah-luas-150-207-ready-harga-murah.html                   
    900     207   150      http://rumahdijual.com/depok/1101162-rumah-mewah-banyak-grratis-nya.html                         
    900     207   150      http://rumahdijual.com/depok/1056912-rumah-luas-type-150-207-siap-huni.html                      
    900     207   150      http://rumahdijual.com/depok/1087893-rumah-luas-type-150-207-pitara-depok.html                   
    900     207   150      http://rumahdijual.com/depok/1115673-rumah-cluster-fuul-bonus.html                               
    900     207   150      http://rumahdijual.com/depok/1064651-cluster-mewah-harga-murah-kota-depok.html                   
    900     207   150      http://rumahdijual.com/depok/1184031-hanya-1-unit-type-207-meter-banyak-bonus-nya.html           
    900     207   130      http://rumahdijual.com/depok/1118213-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html    
    900     207   130      http://rumahdijual.com/depok/1118220-rumah-luas-dekat-jalan-raya-di-pitara.html                  
    900     207   130      http://rumahdijual.com/depok/1118228-promo-tutup-tahun.html                                      
    900     207   130      http://rumahdijual.com/depok/1118231-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html    
    900     207   130      http://rumahdijual.com/depok/1118241-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html    
    900     207   130      http://rumahdijual.com/depok/1118235-hunian-luas-banyak-bonus-di-jalan-pitara-raya.html          
    900     207   130      http://rumahdijual.com/depok/1115602-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html    
    900     207   130      http://rumahdijual.com/depok/1118200-promo-tutup-tahun.html                                      
    900     207   130      http://rumahdijual.com/depok/1115564-rumah-luas-full-granit-banyak-bonusnya.html                 
    900     207   130      http://rumahdijual.com/depok/1133838-rumah-luas-full-granit-banyak-bonusnya.html                 
    900     207   130      http://rumahdijual.com/depok/1185969-rumah-cluster-depok-pitara-raya.html                        
    900     207   130      http://rumahdijual.com/depok/1118196-rumah-luas-dekat-jalan-raya-di-pitara.html                  
    900     207   130      http://rumahdijual.com/depok/1115759-rumah-luas-dekat-jalan-raya-di-pitara.html                  
    900     207   130      http://rumahdijual.com/depok/1133844-rumah-luas-full-granit-banyak-bonusnya.html                 
    900     207   130      http://rumahdijual.com/depok/1074141-rumah-cluster-lt-207-harga-nego-keras-depoo.html            
    900     207   130      http://rumahdijual.com/depok/1118617-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html    
    900     207   130      http://rumahdijual.com/depok/1115763-rumah-luas-dekat-jalan-raya-di-pitara.html                  
    900     207   130      http://rumahdijual.com/depok/1115740-promo-tutup-tahun.html                                      
    900     207   130      http://rumahdijual.com/depok/1118567-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html    
    900     207   130      http://rumahdijual.com/depok/1118564-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html    
    900     207   130      http://rumahdijual.com/depok/1118561-rumah-luas-full-granite-dan-carport-masuk-dua-mobil.html    
    900     207   130      http://rumahdijual.com/depok/1118557-promo-tutup-tahun.html                                      
    900     207   130      http://rumahdijual.com/depok/1074081-rumah-mewah-harga-murah-depok.html                          
    900     207   130      http://rumahdijual.com/depok/1182818-tahap-pembangunan-rumah-luas-di-pitara-depok.html           
    900     207   130      http://rumahdijual.com/depok/1117817-rumah-non-kpr.html                                          
    900     207   130      http://rumahdijual.com/depok/1182803-rumah-pitara-tanah-luas-bangunan-memuaskan.html             
    900     200   190      http://rumahdijual.com/depok/549506-rumah-asri-di-cinangka-depok.html                            
    900     188   180      http://rumahdijual.com/depok/1178319-rumah-dijual-cilondong-900jt.html                           
    900     185   145      http://rumahdijual.com/depok/1149207-jual-rumah-komplek-pelni-depok-harga-di-bawah-pasaran.html  
    900     182   230      http://rumahdijual.com/depok/805755-rumah-lt-182-lb-230-di-villa-pertiwi-depok.html              
    900     180   170      http://rumahdijual.com/depok/1029836-rumah-asri-bernuansa-bali-di-permata-depok-jual-cepat.html  
    900     180   120      http://rumahdijual.com/depok/1160809-dijual-rumah-pinggir-jalan-raya.html                        
    900     156   240      http://rumahdijual.com/depok/950742-komp-marinir-dekat-kubah-mas-limo-depok.html                 
    900     150   150      http://rumahdijual.com/depok/1125314-rumah-besar-harga-kecil.html                                
    900     150   120      http://rumahdijual.com/depok/709158-dijual-rumah-nuansa-asri-bebas-banjir-akses-mudah-lt.html    
    905     326   180      http://rumahdijual.com/depok/1022683-dijual-rumah-3-kontrakan-shm-tanpa-perantara-bisa-nego.html 
    925     150   230      http://rumahdijual.com/depok/1222351-rumah-di-jual-cepat-di-dongkal-sukatani-cimanggis-depok.html
    


```python
selectModerate(df, avg, unit)
```

    
    MODERATE PRICE
    -----------------
    is when the price is above average: 946 (million IDR) with above-average land: 145 (square meters) and above-average building: 119 (square meters)
    
    
    There are : 86  items with above-average price and above-average land.
    
    There are : 56  items with above-average price, above-average land and above-average building.
    
    price  land building                                                                                                     url
    950     577   200      http://rumahdijual.com/depok/1281818-rumah-second-950-juta-pitara-depok.html                         
    950     577   200      http://rumahdijual.com/depok/1308096-rumah-lama-dengan-halaman-luas-di-pancoran-mas-depok.html       
    950     413   250      http://rumahdijual.com/depok/1081645-bu-rumah-luas-sangat-murah-di-sawangan-siap-huni.html           
    950     400   200      http://rumahdijual.com/depok/907308-rumah-luas-di-depok.html                                         
    950     300   200      http://rumahdijual.com/depok/1022522-rumah-dijual-didaerah-depok.html                                
    950     300   150      http://rumahdijual.com/depok/832684-rumah-dan-kontrakan.html                                         
    950     282   268      http://rumahdijual.com/depok/1297940-rumah-di-jual-di-depok-cilodong-10-menit-ke.html                
    950     261   200      http://rumahdijual.com/depok/1044564-rumah-murah-di-daerah-depok-ii.html                             
    950     250   200      http://rumahdijual.com/depok/1283401-rumah-dibeji-depok.html                                         
    950     250   200      http://rumahdijual.com/depok/1263696-rumah-7-kontrakan-cagar-alam-depok.html                         
    950     249   222      http://rumahdijual.com/depok/1040561-rumah-dijualpada-area-depok-dekat-dengan-rencana-tol-cijago.html
    950     243   200      http://rumahdijual.com/depok/941927-rumah-huk-murah-dengan-taman-depan-yang-luas.html                
    950     236   150      http://rumahdijual.com/depok/751860-rumah-minimalis-ukuran-besar-akses-gandul-cinere-pdk-labu.html   
    950     207   150      http://rumahdijual.com/depok/1101624-dijual-rumah-luas-tanah-207-meter-bangunan-150-meter.html       
    950     194   180      http://rumahdijual.com/depok/1052339-kos-kos-6-pintu-murah-strategis.html                            
    950     173   140      http://rumahdijual.com/depok/1092020-rumah-2-lantai-murah-di-pancoran-mas-depok.html                 
    950     166   200      http://rumahdijual.com/depok/1233506-rumah-strategis-tanah-baru-depok.html                           
    950     161   170      http://rumahdijual.com/depok/962536-villa-pertiwi-estate-buktikan-sendiri.html                       
    950     160   140      http://rumahdijual.com/depok/905908-komplek-pelni-cimanggis-depok-dekat-tol.html                     
    950     156   140      http://rumahdijual.com/depok/1065664-rumah-di-komplek-pelni-cimanggis-depok.html                     
    950     150   150      http://rumahdijual.com/depok/982150-di-jual-rumah-minimalis-siap-huni-di-depok-timur.html            
    960     274   180      http://rumahdijual.com/depok/1067157-dijual-rumah-hunian-strategis-di-kp-serab-depok.html            
    970     620   192      http://rumahdijual.com/depok/831529-dijual-rumah-di-kawasan-duren-mekar-kecamatan-bojong-sari.html   
    975     215   180      http://rumahdijual.com/depok/1231667-kontrakan-6-pintu-di-cinere-depok.html                          
    975     190   270      http://rumahdijual.com/depok/1100083-rumah-mewah-murah-depok.html                                    
    975     190   270      http://rumahdijual.com/depok/1108423-rumah-mewah-murah-depok.html                                    
    975     180   155      http://rumahdijual.com/depok/1198842-rumah-mewah-di-sawangan-depok.html                              
    975     180   135      http://rumahdijual.com/depok/1136364-rumah-mewah-terbaik-dekat-tol-cijago-mesjid-kubah-mas.html      
    975     146   200      http://rumahdijual.com/depok/707609-komplek-bukit-cengkeh-1-cimanggis-depok.html                     
    976     165   169      http://rumahdijual.com/depok/39845-dijual-rumah-di-cinere.html                                       
    980     254   220      http://rumahdijual.com/depok/1162368-rumah-dijual-murah-jl-raden-saleh-sukmajaya-depok.html          
    980     250   200      http://rumahdijual.com/depok/1266148-rumah-bangunan-baru-bebas-banjir.html                           
    980     215   180      http://rumahdijual.com/depok/1136997-rumah-siap-huni-murah-dekat-tol-cijago-di-tanah.html            
    980     200   150      http://rumahdijual.com/depok/1204175-rumah-mewah-murah-13-menit-ke-stasiun-depok.html                
    980     200   150      http://rumahdijual.com/depok/1204717-rumah-murah-di-depok-lokasi-strategis.html                      
    985     155   135      http://rumahdijual.com/depok/1083440-rumah-besar-siap-huni-2-lantai.html                             
    985     155   135      http://rumahdijual.com/depok/1261176-rumah-lantai-2-siap-huni-bisa-kpr.html                          
    990     255   240      http://rumahdijual.com/depok/318110-rumah-dua-lantai-dengan-halaman-yang-cukup-luas-dgn.html         
    990     250   150      http://rumahdijual.com/depok/505577-rumah-baru-asri-nyaman-strategis-di-depok.html                   
    990     225   200      http://rumahdijual.com/depok/1000873-rumah-dekat-tol-cisalak-cimanggis-jl-raya-bogor-dan.html        
    998     165   150      http://rumahdijual.com/depok/1094453-perumahan-kalibaru-permai-depok.html                            
    1000    287   200      http://rumahdijual.com/depok/863563-rumah-kontrakan-3-unit-di-beji-depok.html                        
    1000    210   190      http://rumahdijual.com/depok/1124907-dijual-kontrakan-6-pintu.html                                   
    1000    200   165      http://rumahdijual.com/depok/1240356-rumah-dijual-cepat.html                                         
    1000    200   128      http://rumahdijual.com/depok/975701-bukit-rivaria-sawangan.html                                      
    1000    187   120      http://rumahdijual.com/depok/1085102-rumah-di-griya-cinere.html                                      
    1000    186   250      http://rumahdijual.com/depok/975466-rumah-di-komplek-wisma-mekarsari-harapan-dua-bisa-kpr.html       
    1000    180   250      http://rumahdijual.com/depok/994630-rumah-hoek-dua-lantai-di-komp-mekarsari-harapan-2-a.html         
    1000    180   170      http://rumahdijual.com/depok/695019-di-jual-rumah-asri-siap-huni-di-permata-depok.html               
    1000    171   300      http://rumahdijual.com/depok/1024275-rumah-hoek-di-di-komplek-mekarsari-harpan-2-bisa.html           
    1000    171   250      http://rumahdijual.com/depok/960500-dijual-cepat-rumah-di-komplek-harapan-2-mekarsari-depok.html     
    1000    171   250      http://rumahdijual.com/depok/1007804-dijual-rumah-di-wisma-harapan-2-cimanggis.html                  
    1000    168   146      http://rumahdijual.com/depok/904377-dijual-rumah-asri-plus-furniture-di-cilodong-depok-timur.html    
    1000    150   250      http://rumahdijual.com/depok/724472-rumah-milyar-di-tengah-pemukiman-mampang.html                    
    1000    150   120      http://rumahdijual.com/depok/1056565-rumah-mewah-di-pitara-depok.html                                
    1000    149   120      http://rumahdijual.com/depok/1244188-rumah-babakan.html
    


```python
selectExpensive(df, avg, unit)
```

    
    EXPENSIVE PRICE
    -----------------
    is when the price is above average: 946 (million IDR) but you only get land below average: 145 (square meters) and building below average: 119 (square meters).
    
    
    
    There are : 97  items that matched the EXPENSIVE category.
    
    price  land building                                                                                                        url
    950     98    112      http://rumahdijual.com/depok/965763-4-unit-rumah-2-lantai-dekat-dengan-srengseng-sawah.html             
    950     97    90       http://rumahdijual.com/depok/1187973-di-jual-rumah-siap-huni-model-minimalis-lokasi-strategis.html      
    950     96    53       http://rumahdijual.com/depok/1106870-ciputra-cluster-citra-lake-sawangan.html                           
    950     94    80       http://rumahdijual.com/depok/1049339-rumah-dijual-di-depok-murah-minimalis.html                         
    950     94    80       http://rumahdijual.com/depok/1042927-rumah-murah-di-tengah-kota-depok.html                              
    950     94    80       http://rumahdijual.com/depok/1118237-rumah-cantik-harga-bersaing-siap-huni-di-depok.html                
    950     92    90       http://rumahdijual.com/depok/1101220-rumah-satu-unit-dalam-claster-3-menit-dari-toll.html               
    950     91    95       http://rumahdijual.com/depok/1307904-cluster-mewah-di-depan-kubah-mas-depok.html                        
    950     87    74       http://rumahdijual.com/depok/1242050-rumah-mewah-anggrek-2-gdc.html                                     
    950     84    100      http://rumahdijual.com/depok/1027822-di-jual-cluster-margoresidence-2-depok.html                        
    950     144   54       http://rumahdijual.com/depok/1221135-rumah-second-di-grand-depok-city-depok.html                        
    950     144   54       http://rumahdijual.com/depok/1207799-di-jual-rumah-siap-huni-tempat-strategis.html                      
    950     140   85       http://rumahdijual.com/depok/777874-hunian-dekat-dengan-fasilitas-umum-kualitas-premium-di-pesona.html  
    950     136   90       http://rumahdijual.com/depok/1281983-rumah-mewah-murah-di-leuwinanggung-depok-jawa-barat.html           
    950     135   60       http://rumahdijual.com/depok/1199405-perumahan-grand-depok-city-depok.html                              
    950     135   60       http://rumahdijual.com/depok/1244395-rumah-luas-dan-strategis-di-perumahan-grand-depok-city.html        
    950     135   100      http://rumahdijual.com/depok/1068312-di-jual-rumah-minimalis-siap-huni-tanpa-renovasi-posisi.html       
    950     125   114      http://rumahdijual.com/depok/971001-investasi-cerdas-untuk-masa-depan-rumah-di-kav-bri.html             
    950     125   110      http://rumahdijual.com/depok/1146395-rumah-di-telaga-golf-sawangan.html                                 
    950     121   83       http://rumahdijual.com/depok/934238-di-jual-rumah-siap-huni.html                                        
    950     120   42       http://rumahdijual.com/depok/982265-rumah-kontrakan-2-pintu-dekat-kampus-ui-di-beji.html                
    950     113   82       http://rumahdijual.com/depok/1208950-rumah-minimalis-modern-di-limo.html                                
    950     113   75       http://rumahdijual.com/depok/1034428-rumah-dijual-di-komplek-jatijajar-depok.html                       
    950     113   75       http://rumahdijual.com/depok/1015687-rumah-dijual-di-jatijajar-depok.html                               
    950     112   80       http://rumahdijual.com/depok/810985-puri-asri-tanah-baru-rumah-cluster-kpr.html                         
    950     112   80       http://rumahdijual.com/depok/810980-rumah-cluster-puri-indah-tanah-baru.html                            
    950     111   100      http://rumahdijual.com/depok/1163822-di-jual-rumah-model-mewah-harga-bersahabat-nempel-grand.html       
    950     106   110      http://rumahdijual.com/depok/1184036-di-jual-rumah-cantik-lingkungan-sangat-bagus.html                  
    950     100   90       http://rumahdijual.com/depok/1041133-rumahh-2-lantai-di-tanah-baru-depok-r21-0335-a.html                
    958     127   110      http://rumahdijual.com/depok/894576-rumah-minimalis-di-daerah-serua-kecamatan-bojongsari-depok.html     
    958     104   110      http://rumahdijual.com/depok/159880-banjaran-residence-jl-banjaran-pucung-cilangkap-depok.html          
    958     104   110      http://rumahdijual.com/depok/1159384-perumahan-sederhana-tapi-mewah-di-banjaran-residence.html          
    960     96    83       http://rumahdijual.com/depok/943509-rumah-mewah-dp-kecil-dikawasan-krukut-limo-ui-trusan.html           
    960     88    80       http://rumahdijual.com/depok/1051206-jual-rumah-baru-cluster-elite-daerah-strategis-depok-cekidot.html  
    960     82    115      http://rumahdijual.com/depok/1092399-rumah-mewah-di-kukusan-beji-depok.html                             
    965     137   60       http://rumahdijual.com/depok/700334-rumah-nyaman-di-grand-depok-city.html                               
    967     100   105      http://rumahdijual.com/depok/1145662-rumah-mewah-murah-dan-strategis.html                               
    967     100   105      http://rumahdijual.com/depok/1274513-rumah-mewah-murah-di-depok.html                                    
    970     82    100      http://rumahdijual.com/depok/1154697-rumah-2-lantai-mewah-hanya-4-unit-kukusan-depok.html               
    970     80    81       http://rumahdijual.com/depok/1143002-rumah-cluster-mewah-dekat-stasiun-di-tanah-baru.html               
    970     103   66       http://rumahdijual.com/depok/1134093-rumah-mewah-cluster-di-tanah-baru-depok.html                       
    975     96    110      http://rumahdijual.com/depok/932899-kukusan-10e-residence.html                                          
    975     78    70       http://rumahdijual.com/depok/1237256-jalan-rawa-pule-ii-nomor-25q-kukusan-beji-depok.html               
    975     135   91       http://rumahdijual.com/depok/1292929-rumah-di-dpalm-residence-depok.html                                
    975     120   75       http://rumahdijual.com/depok/1067583-dijual-rumah-banjaran-village-a3-no-3-fully-furnished.html         
    980     96    83       http://rumahdijual.com/depok/902980-cluster-fontana-residence.html                                      
    980     140   100      http://rumahdijual.com/depok/423991-rumah-asri-di-tamansari-puri-bali.html                              
    980     131   80       http://rumahdijual.com/depok/947098-rumah-dijual-di-depok-dalam-perumahan-grand-depok-city.html         
    980     131   80       http://rumahdijual.com/depok/930063-dijual-rumah-di-grand-depok-city-murah-0812-8781-a.html             
    980     125   60       http://rumahdijual.com/depok/1296514-07-di-jual-hunian-asri-perumahan-bellacasa-depok.html              
    980     120   60       http://rumahdijual.com/depok/1104603-di-jual-murah-rumah-semi-furnished.html                            
    980     120   100      http://rumahdijual.com/depok/912904-dijual-rumah-2-lantai-kamar-4-dekat-stasiun-depok.html              
    980     102   94       http://rumahdijual.com/depok/914324-tamanna-town-house-sawangan.html                                    
    983     90    89       http://rumahdijual.com/depok/1246835-dijual-murah-cluster-dipermata-kelapa-2-depok-dikomplek-asrama.html
    983     89    90       http://rumahdijual.com/depok/1250970-rumah-murah-2-lantai-di-depok-kode-rmh010.html                     
    983     72    75       http://rumahdijual.com/depok/1069739-rumah-twon-house-kawasan-depok-siap-huni.html                      
    984     120   83       http://rumahdijual.com/depok/1005597-rumah-dalam-komplek-yve-habitat-limo.html                          
    985     91    105      http://rumahdijual.com/depok/1220688-rumah-minimalis-2-lt-di-kawasan-islami-kubah-emas.html             
    985     91    105      http://rumahdijual.com/depok/1199650-rumah-mewah-nuansa-islami.html                                     
    985     86    75       http://rumahdijual.com/depok/877123-perumahan-tanah-baru-depok-2015-a.html                              
    985     84    80       http://rumahdijual.com/depok/799610-hunian-private-strategis-disamping-raffleshill-cibubur.html         
    985     84    80       http://rumahdijual.com/depok/798204-hunian-stategis-mewah-disamping-raffleshill-cibubur.html            
    985     105   91       http://rumahdijual.com/depok/1307308-rumah-cluster-nuansa-islami-dekat-masjid-kubah-emas-depok.html     
    986     86    75       http://rumahdijual.com/depok/877108-rumah-cluster-siap-huni-tanah-baru-dekat-stasiun.html               
    988     104   110      http://rumahdijual.com/depok/331580-perumahan-banjaran-residence-harga-terjangkau-lokasi-strategis.html 
    989     91    105      http://rumahdijual.com/depok/1302441-rumah-exclusive-kubah-mas-cinere-depok.html                        
    989     91    105      http://rumahdijual.com/depok/1211860-rumah-exclusive-samping-masjid-kubah-mas-cinere.html               
    990     98    110      http://rumahdijual.com/depok/994847-rumah-baru-pinggir-jalan-dalam-cluster-di-kukusan-depok.html        
    990     70    105      http://rumahdijual.com/depok/1288716-rumah-mewah-dalam-cluster-di-rtm-kelapa-dua-depok.html             
    990     112   63       http://rumahdijual.com/depok/1154949-rumah-nyaman-dekat-masjid-kubah-mas-depok.html                     
    992     120   100      http://rumahdijual.com/depok/889596-rumah-nyaman-cinere-limo.html                                       
    995     84    90       http://rumahdijual.com/depok/1110911-new-kemang-swatama-depok-residence.html                            
    995     120   60       http://rumahdijual.com/depok/1245595-di-jual-rumah-minimalis-siap-huni-tanpa-renovasi-di.html           
    998     98    100      http://rumahdijual.com/depok/840833-rumah-tingkat-minimalis-berkualitas-depok.html                      
    998     144   60       http://rumahdijual.com/depok/1159830-rumah-di-grand-depok-city.html                                     
    999     144   54       http://rumahdijual.com/depok/1012070-grand-depok-city-sp-206-a.html                                     
    999     144   54       http://rumahdijual.com/depok/1066556-rumah-di-grand-depok-city-boulevard-cluster.html                   
    999     138   113      http://rumahdijual.com/depok/912615-rumah-bumi-cimanggis-indah-hadap-fasilitas-umum-suasana-tenang.html 
    1000    92    110      http://rumahdijual.com/depok/973836-rumah-griya-bukit-cinere.html                                       
    1000    91    108      http://rumahdijual.com/depok/1145209-rumah-murah-cimanggis-depok.html                                   
    1000    90    85       http://rumahdijual.com/depok/951514-rumah-2-lantai-mewah-di-beji-samping-kampus-ui.html                 
    1000    90    68       http://rumahdijual.com/depok/735797-rumah-cantik-di-cluster-acacia.html                                 
    1000    90    68       http://rumahdijual.com/depok/804341-rumah-baru-2-lantai-di-grand-depok-city-gdc.html                    
    1000    90    68       http://rumahdijual.com/depok/1105829-grand-depok-city-cluster-acacia.html                               
    1000    87    110      http://rumahdijual.com/depok/802418-rumah-baru-dekat-depok-town-center-dtc.html                         
    1000    83    96       http://rumahdijual.com/depok/1241307-hunian-asri-di-cinere-fontana-residence.html                       
    1000    80    85       http://rumahdijual.com/depok/947370-exclusive-town-house-cinere-blok-f.html                             
    1000    80    85       http://rumahdijual.com/depok/929876-dijual-rmh-brand-new-minimalis-di-cinere.html                       
    1000    76    115      http://rumahdijual.com/depok/1294229-rumah-second-kelapa-dua.html                                       
    1000    6     97       http://rumahdijual.com/depok/1195544-dijual-rumah-beji-depok.html                                       
    1000    141   36       http://rumahdijual.com/depok/1116154-rumah-hook-wilayah-depok-tipe-36-141m2.html                        
    1000    135   70       http://rumahdijual.com/depok/887336-rumah-2-lantai-baru-strategis-depok-trans-cyber-kalimulya.html      
    1000    132   55       http://rumahdijual.com/depok/1228957-rumah-baru-di-pancoran-mas-depok.html                              
    1000    123   75       http://rumahdijual.com/depok/1100673-di-jual-rumah-mewah-siap-huni-suasana-alam-di.html                 
    1000    120   100      http://rumahdijual.com/depok/1057834-hunian-2-lantai-akses-dekat-perencanaan-tol-pitara-jembatan.html   
    1000    113   80       http://rumahdijual.com/depok/818975-rumah-ditanah-perbatasan-jaksel-dan-depok.html                      
    1000    100   80       http://rumahdijual.com/depok/745301-rumah-dijalan-raya-juanda-depok.html
    

## House Price Between 1000 - 1100 Mio IDR

### Visualize Data


```python
df = visualizeData('depok', 1000, 1100);
```


![png](png/output_95_0.png)


### Analyze the Data of House Price Between 1000 - 1100 Mio IDR


```python
avg = averageMeasures(df)
```

    
    AVERAGE MEASURES
    -----------------
    
    building   124
        land   146
       price  1048
    


```python
mostSpacious(df)
```

    
    MOST SPACIOUS LAND
    -----------------
    
        bath     2
         bed     3
    building   500
        land   750
       price  1100
         url   http://rumahdijual.com/depok/1049422-rumah-750-meter-kontrakan-7-pintu-di-cilangkap-depok.html
    
    MOST SPACIOUS BUILDING
    -----------------
    
        bath     2
         bed     3
    building   500
        land   750
       price  1100
         url   http://rumahdijual.com/depok/1049422-rumah-750-meter-kontrakan-7-pintu-di-cilangkap-depok.html
    


```python
selectEconomical(df, avg, unit)
```

    
    MOST ECONOMICAL
    -----------------
    is when the price is really below average: 1048 (million IDR) but you get above the average land: 146 (square meters) and above the average building: 124 (square meters)
    
    You are blessed to choose one of these 14  houses:
    
    price  land building                                                                                                 url
    1000    287   200      http://rumahdijual.com/depok/863563-rumah-kontrakan-3-unit-di-beji-depok.html                    
    1000    210   190      http://rumahdijual.com/depok/1124907-dijual-kontrakan-6-pintu.html                               
    1000    200   165      http://rumahdijual.com/depok/1240356-rumah-dijual-cepat.html                                     
    1000    200   128      http://rumahdijual.com/depok/975701-bukit-rivaria-sawangan.html                                  
    1000    186   250      http://rumahdijual.com/depok/975466-rumah-di-komplek-wisma-mekarsari-harapan-dua-bisa-kpr.html   
    1000    180   250      http://rumahdijual.com/depok/994630-rumah-hoek-dua-lantai-di-komp-mekarsari-harapan-2-a.html     
    1000    180   170      http://rumahdijual.com/depok/695019-di-jual-rumah-asri-siap-huni-di-permata-depok.html           
    1000    171   300      http://rumahdijual.com/depok/1024275-rumah-hoek-di-di-komplek-mekarsari-harpan-2-bisa.html       
    1000    171   250      http://rumahdijual.com/depok/1007804-dijual-rumah-di-wisma-harapan-2-cimanggis.html              
    1000    171   250      http://rumahdijual.com/depok/960500-dijual-cepat-rumah-di-komplek-harapan-2-mekarsari-depok.html 
    1000    168   146      http://rumahdijual.com/depok/904377-dijual-rumah-asri-plus-furniture-di-cilodong-depok-timur.html
    1000    150   250      http://rumahdijual.com/depok/724472-rumah-milyar-di-tengah-pemukiman-mampang.html                
    1020    187   140      http://rumahdijual.com/depok/896991-dijual-cepat-rumah-di-jatijajar-asri.html                    
    1030    280   200      http://rumahdijual.com/depok/247297-rumah-dijual-dekat-tol-cibubur.html
    


```python
selectModerate(df, avg, unit)
```

    
    MODERATE PRICE
    -----------------
    is when the price is above average: 1048 (million IDR) with above-average land: 146 (square meters) and above-average building: 124 (square meters)
    
    
    There are : 33  items with above-average price and above-average land.
    
    There are : 20  items with above-average price, above-average land and above-average building.
    
    price  land building                                                                                                       url
    1050    448   179      http://rumahdijual.com/depok/1011140-rumah-asri-di-bojong-sari.html                                    
    1060    150   200      http://rumahdijual.com/depok/1176103-cluster-exclusive-strategis-asri-di-cilangkap-cimanggis-depok.html
    1080    325   210      http://rumahdijual.com/depok/968953-rumah-di-dekat-gdc-tanah-luas.html                                 
    1100    750   500      http://rumahdijual.com/depok/1049422-rumah-750-meter-kontrakan-7-pintu-di-cilangkap-depok.html         
    1100    310   150      http://rumahdijual.com/depok/1248664-rumah-dijual-di-cinangka-sawangan-depok.html                      
    1100    300   200      http://rumahdijual.com/depok/1240276-dijual-sangat-cepat-rumah-kokoh-dan-asri-di-meruyung.html         
    1100    272   250      http://rumahdijual.com/depok/981920-rumah-murah-di-cimanggis-depok.html                                
    1100    253   210      http://rumahdijual.com/depok/1258722-dijual-rumah-di-meruyung-depok.html                               
    1100    231   200      http://rumahdijual.com/depok/1299536-jual-rumah-di-depok-i-satu-siap-huni-dan.html                     
    1100    229   150      http://rumahdijual.com/depok/1095649-rumah-asri-dan-nyaman-di-cimpaeun-tapos-depok.html                
    1100    220   165      http://rumahdijual.com/depok/1249089-dijual-rumah-beserta-furniture-di-cilodong-kostrad-depok.html     
    1100    200   200      http://rumahdijual.com/depok/1224181-rumah-telaga-golf.html                                            
    1100    200   125      http://rumahdijual.com/depok/720848-rumah-di-jl-jati-2-depok-timur.html                                
    1100    181   160      http://rumahdijual.com/depok/1063337-rumah-komplek-bbm-asri.html                                       
    1100    180   200      http://rumahdijual.com/depok/993712-butuh-cepat-dijual-murah-sebuah-hunian-exclusive.html              
    1100    177   230      http://rumahdijual.com/depok/994957-perumnas-depok-utara-dekat-ui-dan-margonda.html                    
    1100    165   200      http://rumahdijual.com/depok/1153806-di-jual-rumah-siap-huni-posisi-hook-di-perumahan.html             
    1100    150   225      http://rumahdijual.com/depok/998629-rumah-mewah-2-lantai-dikawasan-cijantung-jakarta-timur.html        
    1100    150   150      http://rumahdijual.com/depok/979165-dijual-cepat-rumah-daerah-depok.html                               
    1100    149   130      http://rumahdijual.com/depok/751101-bellacassa-residence-tole-iskandar-depok.html
    


```python
selectExpensive(df, avg, unit)
```

    
    EXPENSIVE PRICE
    -----------------
    is when the price is above average: 1048 (million IDR) but you only get land below average: 146 (square meters) and building below average: 124 (square meters).
    
    
    
    There are : 49  items that matched the EXPENSIVE category.
    
    price  land building                                                                                                           url
    1050    98    83       http://rumahdijual.com/depok/835986-town-house-exclusive-di-selatan-jakarta.html                           
    1050    90    68       http://rumahdijual.com/depok/1040458-rumah-s-siap-huni-di-grand-depok-city.html                            
    1050    90    68       http://rumahdijual.com/depok/1065414-rumah-take-over-bisa-cash-apa-lagi.html                               
    1050    90    100      http://rumahdijual.com/depok/1230174-rumah-dlm-cluster-permata-kelapa-dua.html                             
    1050    90    100      http://rumahdijual.com/depok/1259816-dijual-rumah-baru-town-house-di-taman-intan-cimanggis.html            
    1050    90    100      http://rumahdijual.com/depok/1259819-rumah-baru-siap-huni-di-jln-radar-auri-cimanggis.html                 
    1050    89    90       http://rumahdijual.com/depok/1144123-hunian-nyaman-dalam-cluster-lokasi-strategis-di-kelapa-dua.html       
    1050    88    80       http://rumahdijual.com/depok/894825-koncept-canti-depan-mall-cinere.html                                   
    1050    126   95       http://rumahdijual.com/depok/1265658-rumah-asri-nuansa-islami-di-depok.html                                
    1050    120   105      http://rumahdijual.com/depok/1314704-di-jual-rumah-2-lantai-tanpa-dp-hunian-exclusive.html                 
    1060    105   60       http://rumahdijual.com/depok/856811-cinere-park-view.html                                                  
    1070    95    85       http://rumahdijual.com/depok/717285-rumah-mewah-siap-huni-di-cinere-depok.html                             
    1080    94    111      http://rumahdijual.com/depok/1080367-rumah-mewah-kalimulya-depok.html                                      
    1080    131   68       http://rumahdijual.com/depok/860425-rumah-premium-cluster-viscani-grand-depok-city.html                    
    1100    99    78       http://rumahdijual.com/depok/972555-rumah-raffles-hills-cibubur-tipe-minimalis-nyaman-dan-asri.html        
    1100    94    90       http://rumahdijual.com/depok/1256512-rumah-lokasi-strategis-nempel-pesona-khayangan-dekat-tol-cijago.html  
    1100    90    85       http://rumahdijual.com/depok/1050067-rumah-mewah-harga-murah-dekat-universitas-indonesia.html              
    1100    90    69       http://rumahdijual.com/depok/1300031-brs-02-rumah-mewah-siap-huni-69-90-acacia.html                        
    1100    88    80       http://rumahdijual.com/depok/994390-brand-new-hunian-markisa.html                                          
    1100    88    80       http://rumahdijual.com/depok/994380-fgc-residence-1-a.html                                                 
    1100    88    80       http://rumahdijual.com/depok/994373-rumah-hunian-cinere.html                                               
    1100    88    80       http://rumahdijual.com/depok/992065-cinere-markisa-residence.html                                          
    1100    88    80       http://rumahdijual.com/depok/451918-dijual-10-unit-rumah-dalam-townhouse.html                              
    1100    80    70       http://rumahdijual.com/depok/1254680-rumah-di-chiera-residence-cinere-harga-1-1-m.html                     
    1100    76    115      http://rumahdijual.com/depok/1235796-rumah-di-kelapa-dua-dekat-kemana-mana.html                            
    1100    70    85       http://rumahdijual.com/depok/581212-itacasa-townhouse-di-margonda-raya.html                                
    1100    15    100      http://rumahdijual.com/depok/936328-dijual-rumah-wisma-cakra-cinere-depok-jakarta-selatan-harga.html       
    1100    140   105      http://rumahdijual.com/depok/1302276-33-di-jual-rumah-mewah-dan-asri-di-bellacasa.html                     
    1100    129   86       http://rumahdijual.com/depok/1133950-di-jual-rumah-tipe-minimalis-baru-1-tahun-pakai.html                  
    1100    127   115      http://rumahdijual.com/depok/1227527-cluster-bellanova-residence-shm-daerah-bojongsari-nyaman-dan-aman.html
    1100    125   120      http://rumahdijual.com/depok/928154-rumah-di-grand-depok-city.html                                         
    1100    124   78       http://rumahdijual.com/depok/1140870-cluster-mewah-di-kelapa-dua-depok.html                                
    1100    122   120      http://rumahdijual.com/depok/730659-di-jual-rumah-cantik-di-depok-2-dekat-juanda.html                      
    1100    121   78       http://rumahdijual.com/depok/1244758-rumah-2-lantai-di-kelapa-dua-depok.html                               
    1100    121   78       http://rumahdijual.com/depok/1245353-rumah-ekslusif-2-lantai-di-depok.html                                 
    1100    121   78       http://rumahdijual.com/depok/1309720-rumah-mewah-dan-strategis-di-depok.html                               
    1100    120   60       http://rumahdijual.com/depok/910324-jual-rumah-bagus-siap-huni-belacassa-tole-iskandar-depok.html          
    1100    120   45       http://rumahdijual.com/depok/1159456-rumah-di-grand-depok-city.html                                        
    1100    120   104      http://rumahdijual.com/depok/1112737-rumah-mewah-murah-dekat-tol-depok-antasari-nilai-investasi.html       
    1100    116   120      http://rumahdijual.com/depok/751095-bellacassa-residence-tole-iskandar-depok.html                          
    1100    114   100      http://rumahdijual.com/depok/1269996-dijual-rumah-di-depok-2-tengah.html                                   
    1100    110   95       http://rumahdijual.com/depok/967317-rumah-dijual-di-grand-depok-city.html                                  
    1100    110   60       http://rumahdijual.com/depok/968082-town-house-dekat-universitas-indonesia-dan-jalan-tol-antasari.html     
    1100    108   70       http://rumahdijual.com/depok/1011238-rumah-keluarga-yang-nyaman-dan-apik-di-kukusan-depok.html             
    1100    108   70       http://rumahdijual.com/depok/1010858-rumah-idaman-keluarga-di-kukusan-depok.html                           
    1100    108   108      http://rumahdijual.com/depok/1227851-jual-rumah-di-sektor-melati-grand-city-depok-jawa.html                
    1100    107   84       http://rumahdijual.com/depok/1236316-grand-pesona-raden-saleh.html                                         
    1100    105   105      http://rumahdijual.com/depok/1046077-rumah-dliving-tanah-baru-depok.html                                   
    1100    100   70       http://rumahdijual.com/depok/1249662-rumah-minimalis-di-sawangan-depok.html
    

## House Price Between 1100 - 1200 Mio IDR


```python
df = visualizeData('depok', 1100, 1200);
```


![png](png/output_103_0.png)


### Analyze the Data of House Price Between 1100 - 1200 mio IDR


```python
avg = averageMeasures(df)
```

    
    AVERAGE MEASURES
    -----------------
    
    building   134
        land   160
       price  1158
    


```python
mostSpacious(df)
```

    
    MOST SPACIOUS LAND
    -----------------
    
        bath     2
         bed     3
    building   500
        land   750
       price  1100
         url   http://rumahdijual.com/depok/1049422-rumah-750-meter-kontrakan-7-pintu-di-cilangkap-depok.html
    
    MOST SPACIOUS BUILDING
    -----------------
    
        bath     2
         bed     3
    building   500
        land   750
       price  1100
         url   http://rumahdijual.com/depok/1049422-rumah-750-meter-kontrakan-7-pintu-di-cilangkap-depok.html
    


```python
selectEconomical(df, avg, unit)
```

    
    MOST ECONOMICAL
    -----------------
    is when the price is really below average: 1158 (million IDR) but you get above the average land: 160 (square meters) and above the average building: 134 (square meters)
    
    You are blessed to choose one of these 17  houses:
    
    price  land building                                                                                                  url
    1100   750    500      http://rumahdijual.com/depok/1049422-rumah-750-meter-kontrakan-7-pintu-di-cilangkap-depok.html    
    1100   310    150      http://rumahdijual.com/depok/1248664-rumah-dijual-di-cinangka-sawangan-depok.html                 
    1100   300    200      http://rumahdijual.com/depok/1240276-dijual-sangat-cepat-rumah-kokoh-dan-asri-di-meruyung.html    
    1100   272    250      http://rumahdijual.com/depok/981920-rumah-murah-di-cimanggis-depok.html                           
    1100   253    210      http://rumahdijual.com/depok/1258722-dijual-rumah-di-meruyung-depok.html                          
    1100   231    200      http://rumahdijual.com/depok/1299536-jual-rumah-di-depok-i-satu-siap-huni-dan.html                
    1100   229    150      http://rumahdijual.com/depok/1095649-rumah-asri-dan-nyaman-di-cimpaeun-tapos-depok.html           
    1100   220    165      http://rumahdijual.com/depok/1249089-dijual-rumah-beserta-furniture-di-cilodong-kostrad-depok.html
    1100   200    200      http://rumahdijual.com/depok/1224181-rumah-telaga-golf.html                                       
    1100   181    160      http://rumahdijual.com/depok/1063337-rumah-komplek-bbm-asri.html                                  
    1100   180    200      http://rumahdijual.com/depok/993712-butuh-cepat-dijual-murah-sebuah-hunian-exclusive.html         
    1100   177    230      http://rumahdijual.com/depok/994957-perumnas-depok-utara-dekat-ui-dan-margonda.html               
    1100   165    200      http://rumahdijual.com/depok/1153806-di-jual-rumah-siap-huni-posisi-hook-di-perumahan.html        
    1120   162    200      http://rumahdijual.com/depok/825264-rumah-siap-huni.html                                          
    1150   335    150      http://rumahdijual.com/depok/1088829-rumah-murah-di-pancoraan-mas-depok.html                      
    1150   200    223      http://rumahdijual.com/depok/1286330-rumah-nyaman-tenang-asri.html                                
    1150   165    200      http://rumahdijual.com/depok/932207-rumah-murah-di-sawangan.html
    


```python
selectModerate(df, avg, unit)
```

    
    MODERATE PRICE
    -----------------
    is when the price is above average: 1158 (million IDR) with above-average land: 160 (square meters) and above-average building: 134 (square meters)
    
    
    There are : 58  items with above-average price and above-average land.
    
    There are : 32  items with above-average price, above-average land and above-average building.
    
    price  land building                                                                                                      url
    1190   200    290      http://rumahdijual.com/depok/1103199-rumah-lelang-bagus-kemang-swatama.html                           
    1190   186    150      http://rumahdijual.com/depok/863907-rumah-baru-dengan-luas-tanah-180-meter-di-cipta.html              
    1200   500    200      http://rumahdijual.com/depok/937327-rumah-asri-diwilayah-kota-depok-cipayung.html                     
    1200   477    300      http://rumahdijual.com/depok/1123298-di-jual-rumah-daerah-cilodong-depok-luas-dan-strategis.html      
    1200   390    250      http://rumahdijual.com/depok/813008-di-jual-rumah-di-cinangka-sawangan-192-a.html                     
    1200   361    180      http://rumahdijual.com/depok/1227652-rumah-kontrakan-4-petak-di-tanah-baru-beji-depok.html            
    1200   324    150      http://rumahdijual.com/depok/1089763-rumah-mewah-di-pitara-depok.html                                 
    1200   289    145      http://rumahdijual.com/depok/1010375-rumah-keluarga-nan-nyaman-di-beji-depok.html                     
    1200   284    220      http://rumahdijual.com/depok/416010-rumah-dijual-beji-depok.html                                      
    1200   262    450      http://rumahdijual.com/depok/1085453-dijual-cepat-butuh.html                                          
    1200   260    160      http://rumahdijual.com/depok/1110866-rumah-nyaman-dan-asri-lokasi-strategis-di-depok.html             
    1200   224    150      http://rumahdijual.com/depok/1153612-rumah-sejuk-luas-akses-tol-cijago-depok-jual-cepat.html          
    1200   220    180      http://rumahdijual.com/depok/201671-dekat-gran-depok-city-murah.html                                  
    1200   220    167      http://rumahdijual.com/depok/1023037-rumah-dijual-di-mampang-pancoran-mas.html                        
    1200   210    300      http://rumahdijual.com/depok/970302-jual-rumah-di-perum-komplek-sawangan-permai-depok-kota.html       
    1200   203    165      http://rumahdijual.com/depok/1019873-rumah-lelang-murah-dibawah-pasar.html                            
    1200   203    165      http://rumahdijual.com/depok/1185446-beji-depok-jual-sewa.html                                        
    1200   200    350      http://rumahdijual.com/depok/1064063-depok-pancoranmas-rumah-idaman-garasi-luas-masuk-4-mobil.html    
    1200   200    350      http://rumahdijual.com/depok/837761-rumah-2-lantai-depok-dekat-stasiun-depok-lama.html                
    1200   200    324      http://rumahdijual.com/depok/918337-rumah-tingkat-super-strategis-super-memukau-harga-terjangkau.html 
    1200   200    324      http://rumahdijual.com/depok/991204-rumah-mewah-harga-murah-di-komplek-besar-mekarsari.html           
    1200   197    390      http://rumahdijual.com/depok/965891-di-jual-rumah-murah-untuk-kost-kostan-dekat-kampus.html           
    1200   194    220      http://rumahdijual.com/depok/946592-dijual-rumah-hunian-asri-kawasan-cimanggis-depok-dengan-akses.html
    1200   192    300      http://rumahdijual.com/depok/1061744-dijual-rumah-2-lantai-posisi-hook-cluster-harga-1-a.html         
    1200   188    200      http://rumahdijual.com/depok/1117010-rumah-dijual-cepat.html                                          
    1200   188    188      http://rumahdijual.com/depok/1050047-rumah-di-tengah-komplek.html                                     
    1200   181    160      http://rumahdijual.com/depok/1062333-rumah-mewah-murah-kavling-bbm-r21-0351-a.html                    
    1200   177    235      http://rumahdijual.com/depok/575578-rumah-di-depok-villa-pertiwi-tong-004-posisi-hook.html            
    1200   173    280      http://rumahdijual.com/depok/664033-rumah-murah-siap-huni-di-perum-bella-casa-depok.html              
    1200   170    150      http://rumahdijual.com/depok/961701-rumah-dekat-margonda-jangan-ragu-pasti-untung.html                
    1200   160    200      http://rumahdijual.com/depok/889530-rumah-siap-huni-daerah-sawangan.html                              
    1200   160    157      http://rumahdijual.com/depok/1080576-rumah-2-lantai-mewah-di-sawangan-r21-0381-a.html
    


```python
selectExpensive(df, avg, unit)
```

    
    EXPENSIVE PRICE
    -----------------
    is when the price is above average: 1158 (million IDR) but you only get land below average: 160 (square meters) and building below average: 134 (square meters).
    
    
    
    There are : 59  items that matched the EXPENSIVE category.
    
    price  land building                                                                                                 url
    1160   131    78       http://rumahdijual.com/depok/1126076-rumah-siap-huni-dua-lantai-pinggir-jalan-raya-pendowo.html  
    1160   121    78       http://rumahdijual.com/depok/1310564-cluster-ekslusif-di-kelapa-dua-depok.html                   
    1160   120    78       http://rumahdijual.com/depok/1262106-cluster-islami-royal-sakinah-di-kelapa-dua-depok-bebas.html 
    1160   115    78       http://rumahdijual.com/depok/1247647-cluster-murah-di-depok.html                                 
    1170   133    78       http://rumahdijual.com/depok/819612-rumah-2-lantai-siap-huni-limo-cinere-dekat-menuju.html       
    1170   133    78       http://rumahdijual.com/depok/1299231-rumah-siap-huni-di-limo-cinere.html                         
    1170   133    78       http://rumahdijual.com/depok/1139047-rumah-menghadap-utara-unit-pojokan-dua-lantai-di-limo.html  
    1170   133    78       http://rumahdijual.com/depok/1128689-rumah-bagus-siap-huni-dua-lantai-menghadap-barat-di.html    
    1170   124    78       http://rumahdijual.com/depok/1245075-hunian-islami-royal-sakinah-kelapa-dua.html                 
    1170   124    78       http://rumahdijual.com/depok/1165033-rumah-cluster-2-lantai-di-kelapa-dua-depok.html             
    1170   124    78       http://rumahdijual.com/depok/1170912-rumah-dijual-di-kelapa-dua-depok-2-lantai-model.html        
    1170   121    78       http://rumahdijual.com/depok/1264649-perumahan-muslim-royal-sakinah-townhouse.html               
    1170   118    110      http://rumahdijual.com/depok/932630-rumah-mewah-dekat-ui-dan-margonda.html                       
    1170   118    110      http://rumahdijual.com/depok/939593-penawaran-perdana-merak-residence-beji.html                  
    1170   102    110      http://rumahdijual.com/depok/855574-rumah-siap-bangun-di-merak-beji-depok.html                   
    1170   95     85       http://rumahdijual.com/depok/874418-rumah-custer-asri-futuristik-dan-murah-di-cinere.html        
    1180   128    110      http://rumahdijual.com/depok/895728-cluster-bernuansa-hijau.html                                 
    1180   100    110      http://rumahdijual.com/depok/777486-rumah-minimalis-2-lantai-sejuk-tenang-dan-strategis.html     
    1190   121    78       http://rumahdijual.com/depok/1125534-cluster-royal-sakinah-beli-sekarang-gratis-biaya-biaya.html 
    1200   153    60       http://rumahdijual.com/depok/998081-rumah-cantik-harga-murah.html                                
    1200   153    130      http://rumahdijual.com/depok/970700-rumah-strategis-dekat-tol-cijago-dan-cibubur-termurah-di.html
    1200   150    80       http://rumahdijual.com/depok/1175414-rumah-di-grand-depok-city.html                              
    1200   150    120      http://rumahdijual.com/depok/858488-dijual-rumah-2-lantai-dekat-stasiun-depok-lama-margonda.html 
    1200   150    105      http://rumahdijual.com/depok/534126-bella-casa-residence-cluster-jasmine-depok.html              
    1200   150    100      http://rumahdijual.com/depok/1265817-rumah-strategis-di-kota-depok-depok-lama-alam-permai.html   
    1200   149    120      http://rumahdijual.com/depok/974731-rumah-dalam-cluster-tugu-residence-tanah-baru-depok.html     
    1200   148    90       http://rumahdijual.com/depok/1149188-jl-haji-dimun-raya-cilodong-depok-jawa-barat.html           
    1200   145    90       http://rumahdijual.com/depok/1012119-rumah-lt-145-lb-90-di-jatijajar-depok-dekat.html            
    1200   145    69       http://rumahdijual.com/depok/1240393-rumah-cantik-2-lantai-di-akasia-terrace-pamulang.html       
    1200   144    60       http://rumahdijual.com/depok/969702-rumah-siap-huni-grand-depok-city-cluster-accacia.html        
    1200   134    113      http://rumahdijual.com/depok/1306180-rumah-aman-dan-nyaman-di-perum-telaga-golf-sawangan.html    
    1200   134    100      http://rumahdijual.com/depok/1305694-rumah-miniamalis-2-lantai-di-telaga-golf-sawangan.html      
    1200   128    78       http://rumahdijual.com/depok/1276386-jual-rumah-nyaman-di-kelapa-dua-depok.html                  
    1200   122    100      http://rumahdijual.com/depok/1305614-rumah-cantik-siap-huni-di-perumahan-sukmajaya-depok-2-a.html
    1200   120    93       http://rumahdijual.com/depok/850597-rumah-di-dalam-cluster-elite-keamanan-24jam.html             
    1200   120    80       http://rumahdijual.com/depok/944700-rumah-di-cluster-anggrek-grand-depok-city-depok.html         
    1200   120    75       http://rumahdijual.com/depok/1244894-viscany-residence-dp-25juta-all.html                        
    1200   120    66       http://rumahdijual.com/depok/1140340-rumah-kokoh-asri-aman-nyaman-natural-strategis.html         
    1200   120    104      http://rumahdijual.com/depok/1269570-rumah-ready-stock-di-akasia-terrace-pondok-petir.html       
    1200   120    100      http://rumahdijual.com/depok/1231682-botania-lake-residence.html                                 
    1200   120    100      http://rumahdijual.com/depok/1028899-rumah-di-megapolitan-blok-m-cinere.html                     
    1200   115    125      http://rumahdijual.com/depok/1230358-rumah-brandnew-di-depok.html                                
    1200   108    90       http://rumahdijual.com/depok/1084815-rumah-di-bukit-cinere-siap-huni-dan-murah.html              
    1200   108    74       http://rumahdijual.com/depok/944490-rumah-mungil-di-depok-kelapadua.html                         
    1200   108    130      http://rumahdijual.com/depok/971222-rumah-90-cinere.html                                         
    1200   108    130      http://rumahdijual.com/depok/1228834-rumah-baru-di-kompperum-bbd-cinere-depok.html               
    1200   105    80       http://rumahdijual.com/depok/1256059-rumah-minimalis-bloulevrd.html                              
    1200   105    60       http://rumahdijual.com/depok/1069883-rumah-di-grand-depok-city-boulevard.html                    
    1200   105    107      http://rumahdijual.com/depok/749103-lumina-hills-residence.html                                  
    1200   104    120      http://rumahdijual.com/depok/1262238-rumah-cantik-hanya-2-unit-di-akasia-terrace.html            
    1200   104    100      http://rumahdijual.com/depok/1008105-rumah-tp-kavling-ui-barat-sejuk-adem-bebas-banjir.html      
    1200   103    123      http://rumahdijual.com/depok/1271071-rumah-minimalis-harga-bagus.html                            
    1200   98     110      http://rumahdijual.com/depok/835278-premium-town-house-di-kavling-ui-depok.html                  
    1200   97     115      http://rumahdijual.com/depok/1239556-rumah-di-cozy-green-cibubur-mansion.html                    
    1200   97     115      http://rumahdijual.com/depok/1135567-cluster-bagus-dan-murah-cozy-green-cibubur-2lt-di.html      
    1200   96     90       http://rumahdijual.com/depok/765290-margonda-residence-one.html                                  
    1200   90     80       http://rumahdijual.com/depok/418961-dijual-rumah-dalam-komplek-dekat-taman.html                  
    1200   90     108      http://rumahdijual.com/depok/1004746-rumah-2-lantai-sangat-strategis-di-depok.html               
    1200   75     80       http://rumahdijual.com/depok/1248757-rumah-mewah-gaya-minimalis-di-kelapa-dua-depok.html
    

## House Price Between 1200 - 1300 Mio IDR

### Visualize the Data


```python
df = visualizeData('depok', 1200, 1300);
```


![png](png/output_112_0.png)


### Analyze the Data of House Price Between 1200 - 1300 Mio IDR


```python
avg = averageMeasures(df)
```

    
    AVERAGE MEASURES
    -----------------
    
    building   145
        land   162
       price  1250
    


```python
mostSpacious(df)
```

    
    MOST SPACIOUS LAND
    -----------------
    
        bath     3
         bed     3
    building   180
        land   580
       price  1250
         url   http://rumahdijual.com/depok/569301-rumah-luas-harga-murah-di-sawangan-depok.html
    
    MOST SPACIOUS BUILDING
    -----------------
    
        bath     2
         bed     4
    building   450
        land   262
       price  1200
         url   http://rumahdijual.com/depok/1085453-dijual-cepat-butuh.html
    


```python
selectEconomical(df, avg, unit)
```

    
    MOST ECONOMICAL
    -----------------
    is when the price is really below average: 1250 (million IDR) but you get above the average land: 162 (square meters) and above the average building: 145 (square meters)
    
    You are blessed to choose one of these 27  houses:
    
    price  land building                                                                                                      url
    1200   500    200      http://rumahdijual.com/depok/937327-rumah-asri-diwilayah-kota-depok-cipayung.html                     
    1200   477    300      http://rumahdijual.com/depok/1123298-di-jual-rumah-daerah-cilodong-depok-luas-dan-strategis.html      
    1200   390    250      http://rumahdijual.com/depok/813008-di-jual-rumah-di-cinangka-sawangan-192-a.html                     
    1200   361    180      http://rumahdijual.com/depok/1227652-rumah-kontrakan-4-petak-di-tanah-baru-beji-depok.html            
    1200   324    150      http://rumahdijual.com/depok/1089763-rumah-mewah-di-pitara-depok.html                                 
    1200   284    220      http://rumahdijual.com/depok/416010-rumah-dijual-beji-depok.html                                      
    1200   262    450      http://rumahdijual.com/depok/1085453-dijual-cepat-butuh.html                                          
    1200   260    160      http://rumahdijual.com/depok/1110866-rumah-nyaman-dan-asri-lokasi-strategis-di-depok.html             
    1200   224    150      http://rumahdijual.com/depok/1153612-rumah-sejuk-luas-akses-tol-cijago-depok-jual-cepat.html          
    1200   220    180      http://rumahdijual.com/depok/201671-dekat-gran-depok-city-murah.html                                  
    1200   220    167      http://rumahdijual.com/depok/1023037-rumah-dijual-di-mampang-pancoran-mas.html                        
    1200   210    300      http://rumahdijual.com/depok/970302-jual-rumah-di-perum-komplek-sawangan-permai-depok-kota.html       
    1200   203    165      http://rumahdijual.com/depok/1019873-rumah-lelang-murah-dibawah-pasar.html                            
    1200   203    165      http://rumahdijual.com/depok/1185446-beji-depok-jual-sewa.html                                        
    1200   200    350      http://rumahdijual.com/depok/1064063-depok-pancoranmas-rumah-idaman-garasi-luas-masuk-4-mobil.html    
    1200   200    350      http://rumahdijual.com/depok/837761-rumah-2-lantai-depok-dekat-stasiun-depok-lama.html                
    1200   200    324      http://rumahdijual.com/depok/991204-rumah-mewah-harga-murah-di-komplek-besar-mekarsari.html           
    1200   200    324      http://rumahdijual.com/depok/918337-rumah-tingkat-super-strategis-super-memukau-harga-terjangkau.html 
    1200   197    390      http://rumahdijual.com/depok/965891-di-jual-rumah-murah-untuk-kost-kostan-dekat-kampus.html           
    1200   194    220      http://rumahdijual.com/depok/946592-dijual-rumah-hunian-asri-kawasan-cimanggis-depok-dengan-akses.html
    1200   192    300      http://rumahdijual.com/depok/1061744-dijual-rumah-2-lantai-posisi-hook-cluster-harga-1-a.html         
    1200   188    200      http://rumahdijual.com/depok/1117010-rumah-dijual-cepat.html                                          
    1200   188    188      http://rumahdijual.com/depok/1050047-rumah-di-tengah-komplek.html                                     
    1200   181    160      http://rumahdijual.com/depok/1062333-rumah-mewah-murah-kavling-bbm-r21-0351-a.html                    
    1200   177    235      http://rumahdijual.com/depok/575578-rumah-di-depok-villa-pertiwi-tong-004-posisi-hook.html            
    1200   173    280      http://rumahdijual.com/depok/664033-rumah-murah-siap-huni-di-perum-bella-casa-depok.html              
    1200   170    150      http://rumahdijual.com/depok/961701-rumah-dekat-margonda-jangan-ragu-pasti-untung.html
    


```python
selectModerate(df, avg, unit)
```

    
    MODERATE PRICE
    -----------------
    is when the price is above average: 1250 (million IDR) with above-average land: 162 (square meters) and above-average building: 145 (square meters)
    
    
    There are : 52  items with above-average price and above-average land.
    
    There are : 32  items with above-average price, above-average land and above-average building.
    
    price  land building                                                                                                        url
    1250   580    180      http://rumahdijual.com/depok/569301-rumah-luas-harga-murah-di-sawangan-depok.html                       
    1250   350    180      http://rumahdijual.com/depok/617728-jual-rumah-hoek-di-perum-buklit-rivaria-sawangan-depok.html         
    1250   240    200      http://rumahdijual.com/depok/1117698-rumah-dipinggir-jalan-raya-kalimulya-r21-0401-a.html               
    1250   200    290      http://rumahdijual.com/depok/1069716-rumah-kemang-swatama-depok-kota.html                               
    1250   172    300      http://rumahdijual.com/depok/1022174-rumah-baru-bagus-kualitas-terbaik-di-komplek-perumahan-mampang.html
    1250   172    219      http://rumahdijual.com/depok/1045862-rumah-mampang-indah-depok.html                                     
    1250   165    250      http://rumahdijual.com/depok/843939-rumah-asri-siap-huni-di-mekarsari-cimanggis-depok.html              
    1250   164    239      http://rumahdijual.com/depok/804413-rumah-perum-mampang-indah-1-panmas-depok.html                       
    1260   200    290      http://rumahdijual.com/depok/1064219-rumah-di-jual-depok-kemang-swatama-depok-residence.html            
    1300   500    300      http://rumahdijual.com/depok/1164169-rumah-mewah-type-300-500-2-lantai-di-jatijajar.html                
    1300   463    150      http://rumahdijual.com/depok/1113877-jual-cepat-banting-harga-jatijajar-depok.html                      
    1300   345    220      http://rumahdijual.com/depok/872898-rumah-dijual-murah-di-depok.html                                    
    1300   306    160      http://rumahdijual.com/depok/895272-jual-rumah-d-complex-harco-depok.html                               
    1300   295    280      http://rumahdijual.com/depok/1246848-jual-rumah-2lantai-siap-huni-strategis.html                        
    1300   294    180      http://rumahdijual.com/depok/958310-rumah-megah-kawasan-depok-dijual-cepat-harga-1-300-a.html           
    1300   268    180      http://rumahdijual.com/depok/984635-di-jual-rumah-mewah-bagus-siap-huni-tanpa-renovasi.html             
    1300   260    200      http://rumahdijual.com/depok/1177020-rumah-minimalis-posisi-hook.html                                   
    1300   257    150      http://rumahdijual.com/depok/1146713-rumah-siap-huni-di-cinere-dengan-harga-minimalis.html              
    1300   240    180      http://rumahdijual.com/depok/1244102-rumah-di-komp-perum-bni-bedahan-sawangan-depok.html                
    1300   236    200      http://rumahdijual.com/depok/1187582-rumah-dijual-daerah-mampang-pancoran-mas-depok.html                
    1300   226    300      http://rumahdijual.com/depok/959942-jual-rumah-di-wisma-cakra-cinere.html                               
    1300   225    150      http://rumahdijual.com/depok/767396-rumah-siap-huni-di-depok.html                                       
    1300   222    186      http://rumahdijual.com/depok/1018555-rumah-second-siap-huni-terawat-dan-nyaman-di-depok.html            
    1300   222    186      http://rumahdijual.com/depok/1027689-rumah-cantik-fully-furnished-kawasan-depok.html                    
    1300   222    186      http://rumahdijual.com/depok/1014384-dijual-rumah-murah-sukmajaya.html                                  
    1300   220    360      http://rumahdijual.com/depok/598809-rumah-di-komplek-perumahan-elit-depok.html                          
    1300   220    150      http://rumahdijual.com/depok/1055197-dijual-segera-rumah-bagus-siap-huni-tp-di-pondok.html              
    1300   215    150      http://rumahdijual.com/depok/830116-rumah-215-meter-tanah-baru-depok-lama.html                          
    1300   177    177      http://rumahdijual.com/depok/846280-rumah-second-terawat-2-lantai-di-depok.html                         
    1300   170    150      http://rumahdijual.com/depok/1139943-dijual-cepat-rumah-siap-pakai.html                                 
    1300   165    160      http://rumahdijual.com/depok/805215-jual-rumah-tingkat-baru-di-jl-meruyung-limo-depok.html              
    1300   164    200      http://rumahdijual.com/depok/698679-rumah-mewah-harga-terjangkau-di-sawangan.html
    


```python
selectExpensive(df, avg, unit)
```

    
    EXPENSIVE PRICE
    -----------------
    is when the price is above average: 1250 (million IDR) but you only get land below average: 162 (square meters) and building below average: 145 (square meters).
    
    
    
    There are : 75  items that matched the EXPENSIVE category.
    
    price  land building                                                                                                            url
    1250   160    140      http://rumahdijual.com/depok/1256655-rumah-mewah-nyaman-di-kelapa-dua-depok.html                            
    1250   160    100      http://rumahdijual.com/depok/900245-rumah-di-jual-di-tanah-baru-depok.html                                  
    1250   156    100      http://rumahdijual.com/depok/996833-di-jual-rumah-cantik-siap-huni-di-ksu-depok.html                        
    1250   156    100      http://rumahdijual.com/depok/1232417-rumah-exlusive-di-dekat-stasiun-depok-r21-0436-a.html                  
    1250   136    110      http://rumahdijual.com/depok/1021175-rumah-siap-huni-kukusan-depok.html                                     
    1250   135    136      http://rumahdijual.com/depok/1208765-rumah-asri-dijual-cepat-di-permata-arcadia-cimanggis.html              
    1250   131    68       http://rumahdijual.com/depok/1293692-grand-depok-city-cluster-acacia-k30.html                               
    1250   129    130      http://rumahdijual.com/depok/478696-puring-townhouse-di-belakang-rs-hermina-depok-lapangan-kamboja.html     
    1250   127    136      http://rumahdijual.com/depok/1038624-rumah-minimalis-dijual-di-tanah-baru-depok.html                        
    1250   127    136      http://rumahdijual.com/depok/1038319-rumah-ready-stock-di-tanah-baru-depok.html                             
    1250   127    136      http://rumahdijual.com/depok/1044858-rumah-dijual-depok.html                                                
    1250   127    136      http://rumahdijual.com/depok/1025757-rumah-ready-stock-dijual-di-tanah-baru-depok.html                      
    1250   127    13       http://rumahdijual.com/depok/1038131-rumah-bagus-di-tanah-baru-depok.html                                   
    1250   110    100      http://rumahdijual.com/depok/681135-rumah-cinere-dlm-townhouse-luas-110mtr.html                             
    1250   100    140      http://rumahdijual.com/depok/1023623-rumah-siap-huni-kukusan-10mnt-dari-pintu-tol-cijago.html               
    1250   100    140      http://rumahdijual.com/depok/1029873-rumah-hunian-dekat-ui-akses-ke-tol-jorr.html                           
    1250   100    140      http://rumahdijual.com/depok/1023047-rumah-baru-4-unit-dekat-akses-dekat-ui.html                            
    1250   100    140      http://rumahdijual.com/depok/1047192-rumah-idaman-dekat-kampus-ui-1-km-ke-tol.html                          
    1250   98     86       http://rumahdijual.com/depok/1023477-rumah-cantik-dan-nyaman-di-sukmajaya-depok.html                        
    1250   96     97       http://rumahdijual.com/depok/1222080-beli-rumah-hadiah-langsung-mobil-hanya-di-cluster-exlusive.html        
    1250   96     97       http://rumahdijual.com/depok/1215152-griyakoe-sawangan-rumah-berkelas-papan-atas.html                       
    1250   96     97       http://rumahdijual.com/depok/1210141-sawangan-depok.html                                                    
    1250   88     105      http://rumahdijual.com/depok/965638-rumah-nyaman-di-lingkungan-asri-di-sawo-griya-kencana.html              
    1250   87     89       http://rumahdijual.com/depok/1194326-rumah-brand-new-di-griyakoe-sawangan.html                              
    1260   90     95       http://rumahdijual.com/depok/918124-townhouse-islami-siap-huni-free-biaya-surat-surat.html                  
    1270   154    110      http://rumahdijual.com/depok/833131-merak-residence-beji-depok.html                                         
    1270   135    100      http://rumahdijual.com/depok/1312651-dijual-rumah-grand-depok-city-anggrek-3-a.html                         
    1270   124    78       http://rumahdijual.com/depok/1165222-cluster-mewah-di-kelapa-dua-depok.html                                 
    1280   90     95       http://rumahdijual.com/depok/990573-cluster-muslim-dekat-cibubur-junction.html                              
    1280   90     95       http://rumahdijual.com/depok/1039814-town-house-dekat-cibubur-junction-grand-madina-cibubur.html            
    1290   120    77       http://rumahdijual.com/depok/1271126-depok-perumahan-grand-depok-city-depok.html                            
    1290   120    115      http://rumahdijual.com/depok/963780-hunian-aman-nyaman-dan-sari.html                                        
    1290   115    112      http://rumahdijual.com/depok/1260486-dijual-town-house-ready-stock-lokasi-strategis-nempel-grand.html       
    1300   160    84       http://rumahdijual.com/depok/518360-rumah-2-lantai-di-pearl-garden-cimanggis-depok-84-a.html                
    1300   160    120      http://rumahdijual.com/depok/1155363-rumah-di-jl-utama-komplek-pelni-cimanggis-depok.html                   
    1300   155    85       http://rumahdijual.com/depok/1124510-rumah-lama-di-komplek-arco.html                                        
    1300   150    55       http://rumahdijual.com/depok/941604-rumah-sawangan-depok.html                                               
    1300   150    55       http://rumahdijual.com/depok/1127038-rumah-idaman-halaman-luas-lokasi-strategis-di-sawangan-depok.html      
    1300   144    60       http://rumahdijual.com/depok/708948-di-jual-rumah-cantik-di-perumahan-grand-depok-city.html                 
    1300   140    125      http://rumahdijual.com/depok/755086-depok-maharaja-pancoran-mas-mampang-sawanganrumah-baru-kawasan-mall.html
    1300   135    92       http://rumahdijual.com/depok/1236334-dijual-rumah-siap-huni-dalam-komplek-asri.html                         
    1300   135    50       http://rumahdijual.com/depok/1006717-taman-dhika-townhouse-cinere.html                                      
    1300   135    132      http://rumahdijual.com/depok/1231082-rumah-siap-huni-dalam-cluster.html                                     
    1300   135    100      http://rumahdijual.com/depok/1156332-rumah-besar-luas-asri-siap-huni-di-puri-depok.html                     
    1300   133    75       http://rumahdijual.com/depok/933279-dijual-rumah-cluster-shm-2-lantai-tanah-baru-depok.html                 
    1300   126    100      http://rumahdijual.com/depok/1050345-rumah-gema-pesona-depok-siap-huni.html                                 
    1300   126    100      http://rumahdijual.com/depok/1042784-rumah-mewah-di-depok.html                                              
    1300   126    100      http://rumahdijual.com/depok/1042746-rumah-depok-siap-huni-mewah.html                                       
    1300   122    110      http://rumahdijual.com/depok/769215-rumah-ternyaman-dan-teraman-buat-keluarga-anda.html                     
    1300   121    115      http://rumahdijual.com/depok/427295-batu-putih-cibubur.html                                                 
    1300   121    104      http://rumahdijual.com/depok/946603-town-house-elah-mansions.html                                           
    1300   120    135      http://rumahdijual.com/depok/1028622-rumah-nyaman-di-lingkungan-tenang-gri10231.html                        
    1300   120    120      http://rumahdijual.com/depok/850946-segera-beli-pasti-untung-dijamin-rumah-mewah-di-hook.html               
    1300   120    115      http://rumahdijual.com/depok/970861-dijual-rumah-minimalis-di-perumahan-telaga-golf-depok.html              
    1300   120    104      http://rumahdijual.com/depok/1224772-cluster-elah-mansion-di-depok.html                                     
    1300   120    104      http://rumahdijual.com/depok/916538-rumah-baru-di-elah-mansions.html                                        
    1300   120    104      http://rumahdijual.com/depok/784836-rumah-di-depok-mewah-dan-nyaman.html                                    
    1300   120    100      http://rumahdijual.com/depok/862519-rumah-hunian-asri-bernuansa-islami-di-cibubur-grand-madina.html         
    1300   115    130      http://rumahdijual.com/depok/1013950-dijual-rumah-didepok-gdc-2-lt-cantik-dan-siap.html                     
    1300   114    100      http://rumahdijual.com/depok/1142128-rumah-2-lantai-dalam-cluster-di-tanah-baru-depok.html                  
    1300   110    110      http://rumahdijual.com/depok/1232944-dijual-rumah-siap-huni-sedang-tersewa-sampai-agustus-2016-a.html       
    1300   110    110      http://rumahdijual.com/depok/1058574-rumah-dijual-di-gandul.html                                            
    1300   108    70       http://rumahdijual.com/depok/1011566-hunian-eksklusif-minimalis-di-kukusan-depok.html                       
    1300   105    120      http://rumahdijual.com/depok/1279933-rumah-inden-dijual-di-kavling-ui-beji-depok.html                       
    1300   105    120      http://rumahdijual.com/depok/1043136-rumah-dijual-cepat.html                                                
    1300   104    110      http://rumahdijual.com/depok/903553-permata-kelapa-dua-hunian-asri-minimalis-dan-strategis.html             
    1300   103    66       http://rumahdijual.com/depok/1159482-rumah-cluster-mewah-di-perbatasan-kota-depok-jakarta.html              
    1300   100    126      http://rumahdijual.com/depok/1009561-rumah-yang-nyaman-di-lokasi-yang-strategis.html                        
    1300   99     144      http://rumahdijual.com/depok/1075824-andar-town-house-jl-portiara-2-cimanggis-depok.html                    
    1300   90     45       http://rumahdijual.com/depok/1236023-cluster-acacia-gdc.html                                                
    1300   90     100      http://rumahdijual.com/depok/1290782-rumah-baru-dan-strategis-dekat-tol-cibubur-dan-tol.html                
    1300   88     80       http://rumahdijual.com/depok/1030921-rumah-dekat-kampus-upn-veteran-jaksel.html                             
    1300   88     80       http://rumahdijual.com/depok/1030906-townhouse-cinere-sisa-4-unit-lagi.html                                 
    1300   88     80       http://rumahdijual.com/depok/1030899-fgc-residence-dekat-fatmawati-jaksel.html                              
    1300   8      93       http://rumahdijual.com/depok/1053536-rumah-mewah-2-lantai-dp-murah-di-pusat-kota.html
    


```python

```

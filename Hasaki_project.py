#!/usr/bin/env python
# coding: utf-8
Hasaki.vn is a system of authorized retail stores for genuine cosmetics and professional beauty services 
with a widespread presence throughout Vietnam. It is currently a strategic distribution partner in the Vietnamese market 
for a range of large brands such as La Roche-Posay, Eucerin, L'oreal, Bioderma, Klairs, Naris Cosmetics, Maybelline, and more.
# In[48]:





# # 1. Import Libraries

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests


# # 2. Web Scraping 

# In[2]:


name = []
en_name = []
discount = []
new_price = []
old_price = []
quantity = []
brand = []


for i in range (1,9):
    website = "https://hasaki.vn/danh-muc/tay-trang-mat-c48.html?p="+str(i)
    response = requests.get(website)
    response.status_code
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('div', {'class' : 'item_sp_hasaki'})

    for result in results:

            # name
            try:
                name.append(result.find('div', {'class':'vn_names'}).get_text()) 
            except:
                name.append('n/a')

            # en name
            try:
                en_name.append(result.find('div', {'class':'en_names'}).get_text())
            except:
                en_name.append('n/a')

            # new_price
            try:
                new_price.append(result.find(class_ ='item_giamoi'))
            except:
                new_price.append('n/a')

            # old price
            try:
                old_price.append(result.find(class_="item_giacu").get_text())
            except:
                old_price.append('0')

            # discount
            try:
                discount.append(result.find(class_="discount_percent2_deal").get_text())
            except:
                discount.append('0')

            # quantity
            try:
                quantity.append(result.find('span', {'class':'item_count_by'}).get_text())
            except:
                quantity.append('0')
                
            #brand
            try:
                brand.append(result.find('div',class_="width_common txt_color_1 space_bottom_3").get_text())
            except:
                brand.append('n/a')


# In[3]:


df = pd.DataFrame({'Name':name,
                   'En_Name':en_name,
                   'Discount':discount,
                   'New_Price':new_price,
                   'Old_Price':old_price,
                   'Quantity':quantity,
                   'Brand':brand})


# In[4]:


df


# In[6]:


df = df.drop_duplicates()


# In[7]:


df


# In[8]:


df.info()


# In[9]:


df['Category_Name'] ='Tẩy trang'


# In[10]:


df


# # 3. Cleaning Data

# In[11]:


df['Variant'] = df['Name'].str.extract(r'(\d+[ml|g])')


# In[12]:


df


# In[13]:


df.info()


# In[14]:


df['Discount'] = df['Discount'].str.replace('%', '')


# In[15]:


df


# In[16]:


df['Old_Price'] = df['Old_Price'].str.replace('₫', '')


# In[17]:


df


# In[18]:


df['Quantity'] = df['Quantity'].str.replace('\n', '')


# In[19]:


df['Brand'] = df['Brand'].str.replace('\n', '')


# In[20]:


df


# In[21]:


df['Discount'] = df['Discount'].astype(str).astype(int)
df['Old_Price'] = df['Old_Price'].str.replace('.', '').astype(int)
df['Quantity'] = df['Quantity'].str.replace('.', '').astype(int)


# In[27]:


df['Quantity'] = df['Quantity'].str.replace('.', '').astype(int)


# In[32]:


df


# In[33]:


df['New_Price'] 


# In[34]:


# Remove non-numeric characters, spaces, and newlines
df['New_Price'] = df['New_Price'].str.replace('<strong class="item_giamoi txt_16">', '', regex=True)


# In[35]:


df['New_Price']


# In[36]:


df['New_Price'] = df['New_Price'].str.replace('</strong>', '', regex=True)
df['New_Price'] = df['New_Price'].str.replace('₫', '')
df['New_Price'] = df['New_Price'].str.replace('.', '').astype(int)


# In[41]:


df


# In[42]:


df.info()


# In[43]:


df


# In[44]:


df.loc[df['Old_Price'] == 0, 'Old_Price'] = df['New_Price']


# In[45]:


df


# In[46]:


df = df.drop_duplicates()


# In[47]:


df


# In[577]:


df.to_excel('hasaki_cleansing.xlsx', index=False)


# In[ ]:





### !!!-DF DIRECTORY, NOT INCLUDED-!!! ###  

df = df_bkup = df()
df.index = pd.to_datetime(df.index).date ; a = df #<<<< TEMPORARY
listed_uniques = df

#> Q1~3 - Percentile, clean & line graph
#> Retrieve the percentile values
listed_uniques = list(each for each in set(listed_uniques['value']))
bottom_2_5 = np.percentile(listed_uniques, 2.5)
top_97_5 = np.percentile(listed_uniques,97.5)
#> And retrive which values will be dropped
percentile_values = [each for each in df['value'] if each <= bottom_2_5 ]
percentile_values = percentile_values + list(each for each in df['value'] if each >= top_97_5)
# percentile_values.sort() #; print(percentile_values)

#> Indexing values to drop
to_drop = []
for each in percentile_values:
    date_value = df.loc[df['value'] == each, 'value']
    date_value = list(date_value.to_dict().keys())[0]
    to_drop.append(date_value)
    # if len(to_drop) == 2: #DEBUGGING ONLY
    #     print(date_value) ; print(to_drop)
# to_drop.sort() #;print(len(to_drop))
#> Dropping & finalizing
df = df.drop(each for each in to_drop)
df_final = df #<<<< TEMPORARY

#> Drawing the 1st graph - Line graph
y_intervals = pd.date_range(start = '2016-07-01', 
                            end = '2020-01-01', 
                            freq = '6ME'
                           )
# plt.xticks(y_intervals)
plt.figure(figsize = (16,5))
plt.xlabel('Date')
plt.ylabel('Page Views')
plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
plt.plot(df.index, df['value'],
         color = 'red'
        )
plt.show()

#> Q4 - Group bar graph
#> Creating the 'Average value' table - Dictionary type
average_df = dict()
for k, v in enumerate(df['value']):
    now_year_month = str(df.index[k])[:7]
    try:
        next_year_month = str(df.index[k+1])[:7]
    except:
        next_year_month = 'END!'

    if k == 0: # first value
        _monthly_values = [v]
        continue
    
    if now_year_month != next_year_month: # every other value(s)
        _monthly_values.append(v)
        year = now_year_month[:4]
        month = calendar.month_name[int(now_year_month[5:])]
        average = np.round(np.mean(_monthly_values), 2)
        average_df.setdefault(year,{})
        average_df[year].setdefault(month)
        average_df[year].update({month:average})
        _monthly_values = []
        continue
    _monthly_values.append(v)
# - End of Dictionary creation - #
#> Creating the 'Average value' table - DataFrame type
years = [each for each in average_df.keys()]
average_data = dict()
for i in range(len(years)):
    if len(average_df[years[i]]) == 12:
        average_data.update({years[i]:[each for each in average_df[years[i]].values()]})
    else:
        month_ranging = [each for each in average_df[years[i]].keys()]
        starting_month_num = month_ranging[0]
        starting_month_num = [mth_num for mth_num, mth_name in enumerate(calendar.month_name) if mth_name == starting_month_num][0]
        average_data.update({years[i]:pd.Series(
                                 [np.float64(each) for each in average_df[years[i]].values()], 
                                 index = [calendar.month_name[each] for each in np.arange(starting_month_num, starting_month_num + len(month_ranging))]
                                 )
                                 })
average_df = pd.DataFrame(data = average_data, index = [calendar.month_name[each] for each in np.arange(1,13)])
average_df = average_df.fillna(0)

#> Drawing the 2nd graph - Group bar graph
bar_width = 0.08
offset = 0
plt.figure(figsize = (8.5,6.5))
for k_num, month in enumerate(average_df.index):
    # print(k, v)
    bar_pos = np.arange(len(years))*2
    plt.bar(bar_pos + offset, average_df.iloc[k_num], bar_width, label = v)
    offset += 0.08
    if k_num == len(average_df.index)-1:
        # print('y')
        xticks = [each + (bar_width*k_num)/2 for each in bar_pos]
        # print(xticks)
        plt.legend(average_df.index, title = 'Months', fontsize = 10)
        plt.title(' ')
        plt.ylabel('Average Page Views')
        plt.xlabel('Years')
        plt.xticks(xticks, years, rotation = 90)
plt.show()

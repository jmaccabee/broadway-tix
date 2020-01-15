# A better way to search for Broadway tickets
*Pain Point:*
The filters available on the Broadway.com website are very limiting.

While users can filter tickets by show, price range and date individually, I searched but couldn't find a way to combine these filters together to find the exact tickets you're looking for. Other ticket marketplaces have more powerful filters, but charge you a higher surcharge in fees for the convenience.

The result is often spending too much time clicking through different performances on the site and usually over paying relative to the "best priced" ticket you want.


*How this app can help*
Enter the `broadway-tix` app. With a few settings provided by the user, the app will scan the entire database of available tickets on the Broadway.com website, loading them into a single Excel file. 

With the powerful filters that come with Excel, you can quickly find the best priced tickets for the show you're looking for. 

Configure the app by providing the date window you're interested in and the "show ID" and "title slug" appearing in the URL when you navigate to the show's calendar page.

For example - a typical calendar page URL will look like this:

`https:checkout.broadway.com/dear-evan-hansen/12547/calendar/`

* `dear-evan-hansen` is the TITLE_SLUG to input in the settings.py file

* `12547` is the SHOW_ID


To launch the app and scan the tickets database, simply execute the `app/bin.py` file using Python 3.

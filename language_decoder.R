# ========================== #
#                            #
# Wikimedia Language Decoder #
#                            #
# ========================== #


# Returns the name of a language associated with a language code used in a 
# Wikimedia project

# based on: https://blog.rstudio.org/2014/11/24/rvest-easy-web-scraping-with-r/

require(rvest)

# save the website
site = read_html('https://en.wikipedia.org/wiki/List_of_Wikipedias')
ltable = site %>%
  html_nodes('div table') %>%
  .[[3]] %>%
  html_table()

# change column names
colnames(ltable) = c('language', 'loc_language', 'id', 'articles', 'pages',
                     'edits', 'admins', 'users', 'act_users', 'images', 'depth')


# fix some variable types
## quick function to get rid off commas that separate thousands
as.numeric2 = function(x) as.numeric(gsub(',', '', x))

ltable$articles = as.numeric2(ltable$articles)
ltable$pages = as.numeric2(ltable$pages)
ltable$edits = as.numeric2(ltable$edits)
ltable$admins = as.numeric2(ltable$admins)
ltable$users = as.numeric2(ltable$users)
ltable$act_users = as.numeric2(ltable$act_users)
ltable$images = as.numeric2(ltable$images)
## fix NAs for depth first: the NA character is \U2014 in hexadecimal
ltable$depth = gsub('\U2014', NA, ltable$depth)
ltable$depth = as.numeric2(ltable$depth)


# create the function
findLanguage = function(language_code) ltable[ltable$id==language_code,
                                              'language']
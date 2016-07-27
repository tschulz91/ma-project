# ======================
# MA Project
# Data analysis
# ======================

# === description === #
# This script is for cleaning and analysing the raw data obtained from
# main.py (or main_cli.py)


# === read data === #
# This whole section doesn't work in R, not efficient enough for my hardware
# Do this in Python (final_aggregation.py) instead
# require(data.table)
# require(zoo)
# require(xts)
# dat = data.table(read.csv('completeData.csv'))
# create the subset of mobile, english articles
# dat_en_mobile = zoo(dat[language=='en' & type=='mw' , visits],
#                     order.by=as.POSIXct(dat[language=='en' & type=='mw' , hour],
#                                         format='%Y-%m-%d %H:%M:%S', tz='GMT'))
# remove non-unique observations by averaging them out
# dat_en_mobile = aggregate(dat_en_mobile, identity, mean)
# create the subset of non-mobile, english articles
# sum up the different types for each hour
# dat_en_nmobile = dat[language!='en' & type=='mw' , sum(visits), by=hour]
# dat_en_nmobile = zoo(dat_en_nmobile$V1,
#                      order.by=as.POSIXct(dat_en_nmobile$hour,
#                                          format='%Y-%m-%d %H:%M:%S', tz='GMT'))
# remove any remaining non-unique observations by averaging them out
# dat_en_nmobile = aggregate(dat_en_nmobile, identity, mean)


# calculated the ratio
# dat_en_ratio = dat_en_mobile / (dat_en_mobile + dat_en_nmobile)
# aggregate to weekly data
# dat_en_ratio_w = apply.weekly(dat_en_ratio, mean)
# plot(dat_en_ratio_w)

require(data.table)
require(zoo)

dat = data.table(read.csv('ratio_en.csv'))
# fix column names
colnames(dat) = c('year', 'week', 'ratio')
# NAs are a ratio of zero
## find the first week when it's not zero anymore
i = 1
while(is.na(dat$ratio[i])) i = i + 1
dat$ratio[1:(i-1)] = 0
# create a year-week column, let day of the week be the last day of the week (7)
dat$yw = paste(dat$year, dat$week, '7', sep='-')
dat$yw = as.POSIXct(dat$yw, tz='GMT', '%Y-%U-%u')

ratio_en = zoo(dat$ratio, order.by = dat$yw)
# remove NAs
ratio_en = ratio_en[!is.na(index(ratio_en))]
plot(ratio_en)

# === Model === #
require(nlstools)

# formulate the standard model
model = ratio_en ~ K/(1+exp(-(a+b*1:length(ratio_en))))
logit_model = nls(model, algorithm = 'port',
                  start = list(K=.5, a=-15, b=.03),
                  lower = list(K=0, a=-Inf, b=-1),
                  upper = list(K=1, a=Inf, b=1))
summary(logit_model)
coefficients(logit_model)
plot(1:length(ratio_en), ratio_en, type='l')
lines(predict(logit_model))

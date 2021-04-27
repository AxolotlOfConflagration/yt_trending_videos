library(RSSL)
library(dplyr)
library(ggplot2)
library(tidyr)

set.seed(1)
df <- read.csv("data/R_chkp4.csv") %>%
  mutate_at('Class', as.factor)
df2<- df_orig %>% add_missinglabels_mar(Class~.,0.95)
g_s4 <- S4VM(Class~.,df,C1=1,C2=0.1,lambda_tradeoff = 3,scale=TRUE,x_center=TRUE)


labs <- g_s4@labelings[-c(1:5),]
colnames(labs) <- paste("Class",seq_len(ncol(g_s4@labelings)),sep="-")
# Adapted from https://github.com/jeknov/EMNLP_17_submission/blob/master/emnlp_data_medians.csv
library(dplyr)
library(reshape2)
library(ggplot2)
library(psych)
require(RJSONIO)
library(jsonlite)
library(irr)

"
File structure:

img,judge,response
185565,0,2
185565,1,4
185565,2,3
284024,0,2
284024,1,2
284024,2,2
"

calculate_icc <- function(csv_file) {
  df_all <- read.csv(csv_file, header=T, col.names=c("img","judge","value"), row.names=NULL)  

  # SA: TODO: ideally should be handled by python script. 
  ######## Subset data by judge: ########
  j1 = df_all %>%
    filter(df_all$judge == 0)
  
  j2 = df_all %>%
    filter(df_all$judge == 1)
  
  j3 = df_all %>%
    filter(df_all$judge == 2)
  
  ######## Subset data by dataset (ds) and system (sys): ########
  ds <- c(as.character(j1$img), as.character(j2$img), as.character(j3$img))
  j1_all <- c(j1$value)
  j2_all <- c(j2$value)
  j3_all <- c(j3$value)
  j_all <- cbind.data.frame(ds, j1_all, j2_all, j3_all)
  
  ######## Calculate intra-class correlation coefficient: ########
  print(icc(j_all[,2:4], unit = "a", conf.level = 0.99, type = "a")) # 0.45, p<0.01
  icc(j_all[,2:4], unit = "a", model = "t") # 0.45, p<0.01
  icc(j_all[,2:4], unit = "a", type="agreement") # 0.45, p<0.01
}

csv_file = "input.csv"
calculate_icc(csv_file)
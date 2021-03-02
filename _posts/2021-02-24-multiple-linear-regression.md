---
layout: post
title: "Multiple Linear Regression with R"
date: 2021-02-24
background: '/img/bg-posts-black-blur.jpg'
---

Multiple linear regression with R
=================================

We demonstrate multiple linear regression (MLR) with R using a case study. Here we perform an “Analysis of grades for an algebra class”. In this case study, we use multiple analytical tools including multiple linear regression, model selection with p-values, and model verification with a test-train split of data.

Objective
---------

Identify predictors of attrition and evaluate methods to measure the difficulty levels of exams

Measuring exam difficulty by comparing the medians
--------------------------------------------------

If the student competence remains constant then exams with similar difficulty levels should have the same median score. The spread of the data, or the standard deviation, however, implies a degree of preparedness or level of understanding among the students. So the standard deviation should decrease over time as the course progresses. We plot the data for MH140 Fall 2019 class and observe the trend that is predicted by logic. The data demonstrate that the tests are of the same difficulty level.

![](https://lh5.googleusercontent.com/XEC0JkSYL_lxzCv6LmLnEV249ZSWO47mBX6zS_xGsS2Dl7JmoNefdMzVfODvAJzDYs_SPwUW_RyOUDUCEsOMhdFNAaINJwIADfP9qFqCvi9fGAx0F1DDjKMp--ppiR2PWsTI697R)

This figure demonstrates that ideally, the median score will remain the same across exams while the standard deviation will decrease over time.

### R code

The preparation of data requires some effort as the LMS(Learning Management Software) exports all data. We have to select only the relevant columns of data, which are the weighted totals of the grading elements. After extracting only the grading element totals, we compile them into an excel spreadsheet and export it to CSV format, which is then imported into R using the following code.

```commandline
> df = read.csv("fall2019.csv")
```
  
Then a boxplot of quiztotal, midterm, final, and Grade is plotted to observe the medians and the standard deviation of the score.

```commandline
> boxplot(df$quiztotal, df$midterm, df$final, df$Grade, 
    + names = c("QuizTotal", "Midterm", "Final", "OverallGrade" ) , 
    + col ="deepskyblue2", ylab="Grades (%)", 
    + main = "Comparing the medians of grading elements")
```

names – labels each boxplot. The names have to be provided as a vector with c(“label1”, “label2”, ..)  
ylab – labels y-axis  
main  – boxplot title  
col – color 

Identifying predictors of attrition
-----------------------------------

We analyze the gradebook data to identify which grading elements can be the best predictors of failure rates in a class. For this, we clean the data and prepare it for analysis for statistical software. Then we performed multiple linear regression on the data using the variable **Grade** (which is the final overall grade that the student receives in the class) as the response variable. The regression is performed against the following variables. 

**HWtotal q1 q2 q3 q4 q5 q6 q7 q8 q9 q10 q11 quiztotal midterm final** 

Results of fitting linear regression models
-------------------------------------------

We can fit against all predictor variables by manually typing in the predictor variables, like this.

```commandline
> lm(Grade ~ HWtotal + quiztotal + midterm + final, data=df)
```

However, instead of fitting the models manually we will first iterate over all possible models.

```commandline
> lapply(colnames(df)\[2:17\], 
    + function(x) summary(lm(paste("Grade", " ~ ", x),
    + data = df))$coefficients)
```

The **lapply**() function extracts the column names, which are the predictor variables, and iteratively sends them to the function fittingly called **function(x)**. Inside the function, **function(x)**, the paste function generates the linear model (e.g. Grade ~ midterm) by pasting the predictor variables passed to it by the **lapply()** function. The **lm()** function then fits the model, and then the **summary()** extracts the coefficients. Here are the results for all possible linear models with one predictor variable. There are two methods of model selection – the p-value method and the adjusted R-squared method. We are going to use the p-value method since it is simpler to implement.  


|             | Estimate    | p-values     |
|-------------|-------------|--------------|
| HWtotal     | 0.6031689   | 0.03585739   |
| q1          | 0.09184575  | 2.06E-01     |
| q2          | 0.1357377   | 1.40E-01     |
| q3          | 0.1258918   | 4.05E-02     |
| q4          | 0.1520878   | 1.17E-04     |
| q5          | 0.08175822  | 4.98E-02     |
| q6          | 0.04201964  | 3.89E-01     |
| q7          | 0.2545848   | 1.08E-03     |
| q8          | 0.06235148  | 3.57E-01     |
| q9          | 0.1817256   | 3.35E-02     |
| q10         | 0.07730769  | 1.20E-01     |
| q11         | 0.03647799  | 4.06E-01     |
| quiztotal   | 0.4686029   | 3.42E-06     |
| midterm     | 0.3968172   | 4.26E-05     |
| final       | 0.4469315   | 0.0045930408 |

From the results, it is clear the _quiz4_, _midterm_, and _quiztotal_ are the best predictors of the final grades. 

Interpretation of results
-------------------------

The following regression models were chosen for their low p-values. 

Model

p-values

Grade ~ midterm

4.26E-05

Grade ~ q4

1.17E-04

Grade ~ HWtotal

0.03586

Grade ~ HWtotal + quiztotal + midterm + final

2.20E-16

Quiztotal is replaced with q4 instead, although quiztotal with the lowest p-value has the highest predictive power. The logic is that, since quiztotal is an aggregate of 11 quizzes, regression against it is really a regression with 11 variables with 10 constraints (the relative coefficients are fixed). We see that the model _Grade ~ HWtotal + quiztotal + midterm + final_ has the best predictive power. However, we only have access to the final grades at the very end of the semester so it is of little value at the beginning of the semester when predicting student success can only be based on a few weeks of data.

The p-values signify that the homework is the worst predictor of the final overall grade while the q4 is the best predictor. This is known to the instructor for some time from experience. The data confirms it statistically. Since the students can use external assistance for their homework assignments, the variable HWtotal has no impact on the final grades. _Quiz 4 consists of solving linear equations. Students who are unable to learn the simple techniques of solving a linear equation, probably do not have the skills or aptitude to learn the more advanced topics in the class. This implies that the student failure rate can be accurately predicted by week 5._

Let us put that theory to test using a test-train stress test to the model. Since the dataset size is so small it is necessary to use bootstrap methods. However, for simplicity, we are going, to begin with, a simple test-train split of the data. In a test-train split, the data is randomly sorted into a training set and a test set according to a predetermined ratio called the **test-train split ratio**. The models are then trained on the training set and then tested on the test set to see which model provides the best fit. We will be fitting linear models only at the beginning, so bias-variance tradeoff does not factor in yet. Later, however, we will generalize to higher dimensional models and explore the bias-variance tradeoff.

### Linear regression using test-train split

We randomly select 80% of the data into a training sample and the remaining 20% is reserved as test data. We train our models on the training samples (which were randomly selected) using the model Grade ~ Quiz4grades which is a linear regression model. 

\> gradefit = lm(Grade ~ q4, data = df, subset = trainset)

Estimate

Std. Error

t -value

p-values

(Intercept)

70.5059

2.59796

27.139

3.64E-14

q4

0.15557

0.03332

4.669

0.000303

### Test the model on the test data set

\> predict(gradefit,df)\[-trainset\]

Student #

3

6

7

17

20

Predicted Grade

86.06334

80.92938

75.63985

75.63985

86.06334

Actual Grade

81

68

74

74

84

Error

\-5.06334

\-12.92938

\-1.63985

\-1.63985

\-2.06334

The MSE (mean squared error) on the test data set is **MSE ~ 40.** The errors are distributed according to the t-distribution. Therefore, the confidence interval for the errors at the 95% CI can be calculated using the t-distribution and they are (-3.4, +1.3).

\> mean(((df$Grade - predict(gradefit,df))\[-trainset\])^2)
40.48838
\> errs = (df$Grade - predict(gradefit,df))
\> mean(errs)
\-1.060716
\> sd(errs)
5.19508
\> mean(errs) + qt(0.975, df=16)\*sd(errs)/sqrt(22)
1.28728
\> mean(errs) - qt(0.975, df=16)\*sd(errs)/sqrt(22)
\-3.408713

  
This means that every prediction the model makes is accurate within -3.4 and 1.3 of the actual grade. The model can be written mathematically as follows.

**Grade = 0.156\*Quiz4grade + 70.5**

This is remarkable since 70 is the passing grade. We see that Quiz 4 performance directly impacts the pass-fail rate. What we have really accomplished is that we have identified the predictor of the attrition rate for this class.

### Observation

The models trained on available data works really well in the same class of students. This means if the first 4 weeks of data are available on a group of students, their future performance can be predicted with 95% accuracy within 3.4 points of the actual final grade.
import pandas as pd
from dash import html, Output, Input, dcc
import plotly.express as px

class GraphBuilder:
    """Contains Method for Building Plot for Dash App."""
    def __init__(self, data="https://raw.githubusercontent.com/ibrahim-ogunbiyi/Loan-Approval-Prediction/main/data/Training%20Dataset.csv"):
        """Read the Data Into a DataFrame."""
        self.df = pd.read_csv(data)
    
    def build_credit_relationship(self):
        """Plot the Relationship Between Credit_History and Loan_Status.

        Returns
        -------
        Plotly Box Figure
        
        """
        mask = pd.crosstab(self.df["Credit_History"], self.df["Loan_Status"]).apply(lambda x: x/x.sum(), axis=1)
        fig = px.bar(
        mask, 
        title= "Relationship between Customer's Credit History VS Loan Status [Proportion]",
        barmode="group"
            )
        fig.update_layout(yaxis_title = "Frequency [Proportion]")
        return(
            dcc.Graph(figure=fig),
            html.P("""Credit history is the number one crucial feature that would allow a
                    customer success in acquiring a loan—as we can see from the above summary,
                    more than 70% of customers with credit history were granted a loan. 
                    The rationale for this is so that the bank can pay attention to the customer's 
                    credit history and determine whether or not the loan is suitable for the consumer."""
                )
        )
    
    def build_propetry_relationship(self):
        """Plot the Relationship between Property Area and Loan Status.
        
        Return
        ------
        Plotly Bar Figure
        """
        mask = pd.crosstab(self.df["Property_Area"], self.df["Loan_Status"]).apply(lambda x: x/x.sum(), axis=1)
        fig = px.bar(
            mask, 
            title= "Relationship between Customer's Property Area VS Loan Status [Proportion]",
            barmode="group"
        )
        fig.update_layout(yaxis_title = "Frequency [Proportion]")
        
        return(
            html.Div([
            dcc.Graph(figure=fig),
            html.P("""According to the above summary, the majority of customers who were eligible loans had property in a semi-urban location.
                As indicated, more than 70% of customers with property in that area were approved for a loan.""")
            ])
        )
    
    def build_app_income_relationship(self):
        """Plot the Relationship of Applicant Income VS Loan Status

        Return
        ------
        Plotly Box Figure
        
        """
        fig = px.box(data_frame=self.df, x= "Loan_Status",
                 y="ApplicantIncome", title = "Relationship of Customer's Loan Status VS Their Income")
        return(
            dcc.Graph(figure=fig),
            html.P("As a customer's income increases, so do their chances of obtaining a loan.")
        )

    def build_loan_amount_relationship(self):
        """Plot the Relationship between Loan Amount and Loan Status

        Return
        ------
        Plotly Box Figure
        
        """
        fig = px.box(data_frame=self.df, x="Loan_Status",
                y = "LoanAmount", title = "Relationship of Customer's Loan Status VS Loan Amount")
        return (
            dcc.Graph(figure=fig),
            html.P("")
        )
    def build_coapplicant_relationship(self):
        fig = px.box(data_frame=self.df, x= "Loan_Status",
                 y="CoapplicantIncome",
                 title = "Relationship of Customer's Loan Status VS Their Co-Applicant Income"
                )
        return (
            dcc.Graph(figure=fig),
            html.P("As a customer's co-applicant income increases, so do their chances of obtaining a loan.")
        )

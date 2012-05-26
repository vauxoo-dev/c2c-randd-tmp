<html>
%if context['data'] and context['data'].get('form'):
  <%form = True%>
%else:
  <%form = False%>
%endif

%if form  and context['data']['form']['display_with_zero_qty'] ==1:
  <%all_zero = True%>
%else:
  <%all_zero = False%>
%endif


 <%
      categ = ''
      stock_account = ''
      expense_account = ''
      cumul_categ_qty = 0.0
      cumul_categ_valuation = 0.0
      cumul_categ_valuation2 = 0.0
      cumul_categ_valuation_diff = 0.0
      cumul_qty = 0.0
      cumul_valuation = 0.0
      cumul_valuation2 = 0.0
      cumul_valuation_diff = 0.0
 %>


<head>
    <style type="text/css">
        ${css}
        pre {font-family:helvetica; font-size:12;}
    </style>
<h1>${_("Product List")}</h1>
</head>
<body>
    <style  type="text/css">
     table {
       width: 100%;
       page-break-after:auto;
       border-collapse: collapse;
       cellspacing="0";
       font-size:10px;
           }
     td { margin: 0px; padding: 3px; border: 1px solid lightgrey;  vertical-align: top; }
     th { margin: 0px; padding: 3px; border: 0px solid lightgrey;  vertical-align: top; }
     pre {font-family:helvetica; font-size:15;}
    </style>
   
<table>

        <thead>
          <tr>
<!--            <th style="text-align:left;white-space:nowrap">${_("Category")}</th> -->
            <th style="text-align:left;white-space:nowrap">${_("Product")}</th>
            <th style="text-align:right;white-space:nowrap">${_("Qty")}</th>
            <th style="text-align:left;white-space:nowrap">${_("UoM")}</th>
            <th style="text-align:right">${_("Valuation")}</th>
            <th style="text-align:right">${_("Valuation Comp")}</th>
            <th style="text-align:right">${_("Valuation Diff")}</th>
<!--            <th style="text-align:left;white-space:nowrap">${_("Code")}</th>  -->
<!--            <th style="text-align:left;white-space:nowrap">${_("Account")}</th>  -->
<!--            <th style="text-align:left;white-space:nowrap">${_("Code")}</th>  -->
<!--            <th style="text-align:left;">${_("Account Expense")}</th>  -->
         </tr>
        </thead>
%for prod in objects :
        <tbody>
%if (all_zero or prod.qty_available !=0  or prod.valuation !=0 or prod.valuation2 !=0 ):

%if categ and categ != prod.categ_id.name:
          <tr>
<!--            <th style="text-align:left;white-space:nowrap"></th> -->
            <th style="text-align:left;white-space:nowrap">${categ} ${_("TOTAL")}</th>
            <th style="text-align:right;white-space:nowrap">${  formatLang(cumul_categ_qty)}</th>
            <th style="text-align:left;white-space:nowrap"></th>
            <th style="text-align:right">${  formatLang(cumul_categ_valuation)}</th>
            <th style="text-align:right">${  formatLang(cumul_categ_valuation2)}</th>
            <th style="text-align:left;white-space:nowrap"></th>
<!--            <th style="text-align:left;white-space:nowrap"></th>  -->
<!--            <th style="text-align:left;white-space:nowrap"></th>  -->
<!--            <th style="text-align:left;white-space:nowrap"></th>  -->
<!--            <th style="text-align:left;"></th>  -->
         </tr>
         <tr>
<!--            <th style="text-align:left;white-space:nowrap"></th> -->
%if cumul_categ_valuation_diff < 0.0:
            <th style="text-align:right;white-space:nowrap">${stock_account} : ${expense_account}</th>
%else:
            <th style="text-align:right;white-space:nowrap">${expense_account} : ${stock_account}</th>
%endif
            <th style="text-align:right;white-space:nowrap"></th>
            <th style="text-align:left;white-space:nowrap"></th>
            <th style="text-align:left;white-space:nowrap"></th>
            <th style="text-align:left;white-space:nowrap"></th>
%if cumul_categ_valuation_diff < 0.0:
            <th style="text-align:right">${  formatLang( -cumul_categ_valuation_diff)}</th>
%else:
            <th style="text-align:right">${  formatLang(cumul_categ_valuation_diff)}</th>
%endif
<!--            <th style="text-align:left;white-space:nowrap"></th>  -->
<!--            <th style="text-align:left;white-space:nowrap"></th>  -->
<!--            <th style="text-align:left;white-space:nowrap"></th>  -->
<!--            <th style="text-align:left;"></th>  -->
         </tr>

 <%
      cumul_categ_qty = 0.0
      cumul_categ_valuation = 0.0
      cumul_categ_valuation2 = 0.0
      cumul_categ_valuation_diff = 0.0
 %>

%endif
          <tr>
<!--            <td style="text-align:left;white-space:nowrap">${prod.categ_id.name or ''}</td> -->
            <td>${prod.name}</td>
            <td style="text-align:right">${prod.qty_available}</td>
            <td>${prod.uom_id.name or ''}</td>
            <td style="text-align:right">${prod.valuation}</td>
            <td style="text-align:right">${prod.valuation2}</td>
            <td style="text-align:right">${prod.valuation_diff}</td>
<!--            <td style="text-align:right">${prod.stock_account_id.code}</td>  -->
<!--            <td>${prod.stock_account_id.name}</td>  -->
<!--            <td style="text-align:right">${prod.expense_account_id.code}</td>  -->
<!--            <td>${prod.expense_account_id.name}</td>  -->

 <%
      categ = prod.categ_id.name
      stock_account = prod.stock_account_id.code + ' ' + prod.stock_account_id.name
      expense_account = prod.expense_account_id.code + ' ' + prod.expense_account_id.name
      cumul_categ_qty += prod.qty_available
      cumul_categ_valuation += prod.valuation
      cumul_categ_valuation2 += prod.valuation2
      cumul_categ_valuation_diff += prod.valuation_diff
      cumul_qty += prod.qty_available
      cumul_valuation += prod.valuation
      cumul_valuation2 += prod.valuation2
      cumul_valuation_diff += prod.valuation_diff
 %>
         </tr>
%endif
        </tbody>
%endfor
        <tfoot>
                  <tr>
<!--            <th style="text-align:left;white-space:nowrap"></th> -->
            <th style="text-align:left;white-space:nowrap">${categ} ${_("TOTAL")}</th>
            <th style="text-align:right;white-space:nowrap">${  formatLang(cumul_categ_qty)}</th>
            <th style="text-align:left;white-space:nowrap"></th>
            <th style="text-align:right">${  formatLang(cumul_categ_valuation)}</th>
            <th style="text-align:right">${  formatLang(cumul_categ_valuation2)}</th>
            <th style="text-align:left;white-space:nowrap"></th>
<!--            <th style="text-align:left;white-space:nowrap"></th>  -->
<!--            <th style="text-align:left;white-space:nowrap"></th>  -->
<!--            <th style="text-align:left;white-space:nowrap"></th>  -->
<!--            <th style="text-align:left;"></th>  -->
         </tr>
         <tr>
<!--            <th style="text-align:left;white-space:nowrap"></th> -->
%if cumul_categ_valuation_diff < 0.0:
            <th style="text-align:right;white-space:nowrap">${stock_account} : ${expense_account}</th>
%else:
            <th style="text-align:right;white-space:nowrap">${expense_account} : ${stock_account}</th>
%endif
            <th style="text-align:right;white-space:nowrap"></th>
            <th style="text-align:left;white-space:nowrap"></th>
            <th style="text-align:left;white-space:nowrap"></th>
            <th style="text-align:left;white-space:nowrap"></th>
%if cumul_categ_valuation_diff < 0.0:
            <th style="text-align:right">${  formatLang( -cumul_categ_valuation_diff)}</th>
%else:
            <th style="text-align:right">${  formatLang(cumul_categ_valuation_diff)}</th>
%endif
<!--            <th style="text-align:left;white-space:nowrap"></th>  -->
<!--            <th style="text-align:left;white-space:nowrap"></th>  -->
<!--            <th style="text-align:left;white-space:nowrap"></th>  -->
<!--            <th style="text-align:left;"></th>  -->
         </tr>

          <tr>
            <th style="text-align:left;white-space:nowrap">${_("GRAND TOTAL")}</th>
<!--            <th style="text-align:left;white-space:nowrap"></th> -->
            <th style="text-align:right;white-space:nowrap">${ formatLang(cumul_qty)}</th>
            <th style="text-align:left;white-space:nowrap"></th>
            <th style="text-align:right">${ formatLang(cumul_valuation)}</th>
            <th style="text-align:right">${ formatLang(cumul_valuation2)}</th>
            <th style="text-align:right">${ formatLang(cumul_valuation_diff)}</th>
<!--           <th style="text-align:left;white-space:nowrap"></th>  -->
<!--           <th style="text-align:left;white-space:nowrap"></th>  -->
<!--           <th style="text-align:left;white-space:nowrap"></th>  -->
<!--           <th style="text-align:left;"></th>  -->
         </tr>
        </tfoot>
</table>

</body>

</html>

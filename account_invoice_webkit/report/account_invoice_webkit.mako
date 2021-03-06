<html>
<head>
    <style type="text/css">
        ${css}
        pre {font-family:helvetica; font-size:12;}
    </style>
</head>

<body>
    <style  type="text/css">
     table {
       width: 100%;
       page-break-after:auto;
       border-collapse: collapse;
       cellspacing="0";
       font-size:12px;
           }
     td { margin: 0px; padding: 3px; border: 1px solid lightgrey;  vertical-align: top; }
     pre {font-family:helvetica; font-size:15;}
    </style>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>

    %for inv in objects :
    <% setLang(inv.partner_id.lang) %>
<br>
    <table  >
<!-- 
****************************
left Address
******************************-->
        %if inv.company_id.address_label_position == 'left':
         <tr>
         <td style="width:50%;height:35mm;font-size:130%;padding-left:5mm;padding-top:3mm">
%if inv.type in ('in_invoice','in_refund'):
${_("Supplier Address")}
<hr>
%endif
${inv.address_invoice_id.address_label|carriage_returns}
         </td>
         <td style="width:50%;padding:0px;font-size:100%;padding-left:5mm;padding-top:3mm">
<table  style="padding:0px;" >
         %if inv.address_invoice_id.phone :
<tr>
<td style="border:none"> ${_("Phone")}</td><td style="border:none"> ${inv.address_invoice_id.phone|entity} </td
</tr>
        %endif
        %if inv.address_invoice_id.fax :
<tr>
<td style="border:none">${_("Fax")}</td><td style="border:none"> ${inv.address_invoice_id.fax|entity} </td>
</tr>
        %endif
        %if inv.address_invoice_id.email :
<tr>
<td style="border:none">${_("Mail")}</td><td style="border:none">${inv.address_invoice_id.email|entity} </td>
</tr>
        %endif
        %if inv.partner_id.vat :
<tr>
<td style="border:none">${_("VAT")}</td><td style="border:none"> ${inv.partner_id.vat|entity} </td>
</tr>
        %endif
</table>
         </td>
        </tr>
        %endif
<!-- 
****************************
right Address
******************************-->
        %if inv.company_id.address_label_position == 'right' or not inv.company_id.address_label_position:
         <tr>
         <td style="width:50%">
<table {border:none} >
         %if inv.address_invoice_id.phone :
<tr>
<td> ${_("Phone")}</td><td> ${inv.address_invoice_id.phone|entity} </td
</tr>
        %endif
        %if inv.address_invoice_id.fax :
<tr>
<td>${_("Fax")}</td><td> ${inv.address_invoice_id.fax|entity} </td>
</tr>
        %endif
        %if inv.address_invoice_id.email :
<tr>
<td>${_("Mail")}</td><td>${inv.address_invoice_id.email|entity} </td>
</tr>
        %endif
        %if inv.partner_id.vat :
<tr>
<td>${_("VAT")}</td><td> ${inv.partner_id.vat|entity} </td>
</tr>
        %endif
</table>
         </td>
         <td style="width:50%">
%if inv.type in ('in_invoice','in_refund'):
${_("Supplier Address")}
<hr>
%endif
${inv.address_invoice_id.address_label|carriage_returns}
         </td>
        </tr>
        %endif

    </table>
    <br>
<!-- folding marks -->
<table style="border:none">
<tr style="border:none">
<td style="text-align:left;border:none">.</td>
<td style="text-align:right;border:none">.</td>
</tr>
</table>

<br>
    %if inv.state in ['proforma','proforma2']:
    <h1 style="clear:both;">${_("ProForma")}</h1> 
    %endif

<table style="width:auto;float:right;font-weight:bold;font-size:140%">
<tr>
  <td style="text-align:right">
    %if inv.type == 'out_invoice' :
      ${_("Customer Invoice")} 
    %elif inv.type == 'in_invoice' :
      ${_("Supplier Invoice")} 
    %elif inv.type == 'out_refund' :
      ${_("Customer Refund")} 
    %elif inv.type == 'in_refund' :
      ${_("Supplier Refund")} 
    %endif
   </td>
   <td  style="text-align:right;">${inv.number or ''|entity}
   </td>
   
</tr>
<tr>
    <td style="text-align:right;">${_("Datum")} </td><td  style="text-align:right;"> ${formatLang(inv.date_invoice, date=True)|entity}</td>
</tr>
<tr>
<td style="border:none"></td>
</tr>
</table>
<br>
    %if inv.state == 'cancel' :
    <h1 style="clear:both;">${inv.state}</h1> 
    <br/>
    %endif
    <table >
        <tr>
          %if inv.name :
            <td>${_("Customer Ref")}</td>
          %endif
          %if not inv.picking_ids and inv.origin:
            <td>${_("Origin")}</td>
          %endif
          %if inv.picking_ids:
            <td>${_("Pickings/Order")}</td>
          %endif
          %if inv.reference:
            <td>${_("Reference")}</td>
          %endif

            <td style="white-space:nowrap">${_("Payment Term")}</td>
            <td style="white-space:nowrap">${_("Due Date")}</td>
            <td>${_("Curr")}</td>
        </tr>
        <tr>
          %if inv.name :
            <td>${inv.name.rfind(':') > 0 and inv.name[:inv.name.rfind(':')] or inv.name}</td>
          %endif

          %if not inv.picking_ids and inv.origin:
            <td>${inv.origin} </td>
          %endif

          %if inv.picking_ids:
            <td style="padding:0px;">
           <table style="border:none;">
          %for pick in inv.picking_ids:
            <tr style="white-space:nowrap;border:none">
             <td style="border:none">${pick.name} / ${formatLang(pick.date, date=True)|entity}</td>
             %if pick.sale_id:
	     <td style="border:none">${pick.sale_id.name} / ${formatLang(pick.sale_id.date_order, date=True)|entity}</td>
             %endif
            </tr>
          %endfor   
           </table> 
            </td>
          %endif

          %if inv.reference :
             <td>${inv.reference}</td>
          %endif

          <td>${inv.payment_term.name or ''}</td>
          <td>${inv.date_due or ''}</td>
         <td>${inv.currency_id.name}</td>
         </tr>
    </table>
  
    <h1><br /></h1>
    <table >
        <thead>
          <tr style=" border-width:1px; border-style:solid;">
%if inv.print_code:
            <th style="text-align:center;border-width:1px; border-style:solid;">${_("Code")}</th>
%endif
            <th style="text-align:center;border-width:1px; border-style:solid;">${_("Description")}</th>
%if inv.print_ean:
            <th style="text-align:center;border-width:1px; border-style:solid;">${_("EAN")}</th>
%endif
            <th style="text-align:center;border-width:1px; border-style:solid;">${_("Taxes")}</th>
            <th style="text-align:center;border-width:1px; border-style:solid;">${_("QTY")}</th>
            <th style="text-align:center;border-width:1px; border-style:solid;">${_("Unit")}</th>
            <th style="text-align:center;white-space:nowrap;border-width:1px; border-style:solid;">${_("Unit Price")}</th>
          %if inv.print_price_unit_id == True:
            <th style="text-align:center;border-width:1px; border-style:solid;">${_("Price/Unit")}</th>
          %endif
          %if inv.amount_discount != 0:
            <th style="text-align:center;border-width:1px; border-style:solid;">${_("Disc.(%)")}</th>
          %endif
            <th style="text-align:center;border-width:1px; border-style:solid;">${_("Price")}</th>
         </tr>
        </thead>
        %for line in inv.invoice_line_sorted :
        <tbody>
        <tr>
%if inv.print_code:
           <td>${line.product_id.default_code or ''|entity}</td>
%endif
           <td>${line.product_id.name or line.name|entity}

%if line.note and len(line.note.replace('\n','')) > 0 :
<br>
<style type="text/css">
note {font-size:75%};
</style>
<note>            ${line.note |carriage_returns} </note>
%endif
</td>
%if inv.print_ean:
            <td>${line.product_id.ean13 or ''}</td>
%endif
           <td>${ ', '.join([ tax.name or '' for tax in line.invoice_line_tax_id ])|entity}</td>
           <td style="white-space:nowrap;text-align:right;">${line.quantity}</td>
           <td style="white-space:nowrap;text-align:left;">${line.uos_id.name or _("Unit")}</td>
           <td style="white-space:nowrap;text-align:right;">${formatLang('price_unit_pu' in line._columns and line.price_unit_pu or line.price_unit,digits=2)}</td>
          %if inv.print_price_unit_id == True:
           <td style="white-space:nowrap;text-align:left;">${line.price_unit_id.name or ''}</td>
          %endif
          %if inv.amount_discount != 0:
           <td style="white-space:nowrap;text-align:right;">${line.discount or 0.00}</td>
          %endif
           <td style="white-space:nowrap;text-align:right;">${formatLang(line.price_subtotal)}
         </td></tr>
        %endfor
        <tr>
           <td colspan="${inv.cols}" style="border-style:none"/>
           <td style="border-top:2px solid;white-space:nowrap"><b>${_("Net Total")}:</b></td>
           <td style="border-top:2px solid;text-align:right">${formatLang(inv.amount_untaxed)}</td>
        </tr>
        <tr>
           <td colspan="${inv.cols}" style="border-style:none"/>
           <td style="border-style:none"><b>${_("Taxes")}:</b></td>
           <td style="text-align:right">${formatLang(inv.amount_tax)}</td></tr>
        <tr> 
           <td colspan="${inv.cols}" style="border-style:none"/>
           <td style="border:2px solid;font-weight:bold;white-space:nowrap">${_("Total")} ${inv.currency_id.name}:</td>
           <td style="border:2px solid;text-align:right;font-weight:bold">${formatLang(inv.amount_total)}</td></tr>
        </tbody>
    </table>
<br>
       %if inv.tax_line :
    <table class="list_table" style="width:40%;border:1px solid grey">
        <tr><th>${_("Tax")}</th><th style="text-align:left;">${_("Base")}</th><th style="text-align:left;">${_("Amount")}</th></tr>
        %for t in inv.tax_line :
        <tr>
            <td style="border:1px solid grey">${ t.name|entity } </td>
            <td style="text-align:right;border:1px solid grey;white-space:nowrap">${ formatLang(t.base)}</td>
            <td style="text-align:right;border:1px solid grey;white-space:nowrap">${ formatLang(t.amount) }</td>
        </tr>
        %endfor
        <tr>
            <td style="border-style:none"/>
            <td style="border-top:0px solid;text-align:right;white-space:nowrap"><b>${_("Total Tax:")}</b></td>
            <td style="border-top:0px solid;text-align:right;white-space:nowrap">${ formatLang(inv.amount_tax) }</td>
        </tr>
        %endif
    </table>        
    %if inv.comment:
     <br>  ${inv.comment|carriage_returns}
    %endif:
    <p style="page-break-after:always"></p>
    %endfor
</body>
</html>

"""Reproduce reviewed locale-parity edits. Run from mh-landing-articles."""
from pathlib import Path
import json,re,subprocess,sys
ROOT=Path('/Users/nathanganser/Documents/Development/mh-landing-articles')
Q=lambda s:json.dumps(s,ensure_ascii=False)
DATA={}
def add(slug,locale,title,intro,takeaways,body,faq=None):
 DATA[(slug,locale)]=(title,intro,takeaways,body,faq)
S='wann-verjahrt-eine-rechnung-schweiz'
add(S,'fr','Prescription des factures en Suisse : les délais',
"En Suisse, une facture ne se prescrit pas systématiquement après trois ans. Le délai ordinaire est de dix ans selon l’art. 127 CO. Des délais plus courts s’appliquent aux créances énumérées à l’art. 128 CO. Le point de départ est l’exigibilité de la créance, selon l’art. 130 CO.",
[('10 ans en principe','L’art. 127 CO prévoit dix ans, sauf disposition spéciale.'),('5 ans dans certains cas','L’art. 128 CO vise notamment les loyers, intérêts, salaires, travaux d’artisans et honoraires de médecins ou d’avocats.'),('Un rappel ne suffit pas','Un rappel, même recommandé, n’interrompt pas la prescription. L’art. 135 CO définit les actes qui l’interrompent.')],
"""## Quel délai retenir pour votre facture ?

La nature de la créance compte davantage que le titre du document. Une facture de projet peut relever du délai ordinaire de dix ans, mais vous devez vérifier si une exception s’applique. Une facturation mensuelle ne suffit pas, à elle seule, à qualifier juridiquement la créance.

| Créance | Délai | Base légale |
|---|---|---|
| Créance sans délai spécial | 10 ans | Art. 127 CO |
| Loyers et intérêts périodiques | 5 ans | Art. 128 ch. 1 CO |
| Travaux d’artisans, honoraires médicaux ou d’avocats, salaires | 5 ans | Art. 128 ch. 3 CO |
| Créance constatée par un acte de défaut de biens, envers le débiteur | 20 ans | Art. 149a LP |

## L’exigibilité marque le départ

L’art. 130 CO fixe le début du délai à l’exigibilité. Conservez le contrat, les conditions de paiement acceptées et la preuve des prestations. La date d’émission de la facture et sa date d’exigibilité peuvent différer.

**Exemple fictif :** une prestation est facturée en juillet avec une échéance convenue en août. Le calcul part de l’exigibilité en août, puis dépend du délai applicable à cette prestation. Un nouveau rappel ne décale pas ce point de départ.

## Comment interrompre la prescription ?

Selon l’art. 135 CO, la reconnaissance de dette par le débiteur et certains actes du créancier, notamment une poursuite, une requête de conciliation ou une action en justice, interrompent la prescription. Une reconnaissance peut aussi résulter d’un paiement partiel ou d’intérêts. Conservez-en la preuve.

Le rappel sert à demander le paiement et peut mettre le débiteur en demeure. Il **n’interrompt pas** la prescription, même avec un nouveau délai. Le [modèle de rappel suisse](/mahnung-vorlage-schweiz) vous aide à formuler la demande, mais ne remplace pas un acte interruptif.

## Gardez un dossier exploitable

Rassemblez contrat, facture, justificatifs des prestations, échéance, échanges et paiements reçus. Vérifiez les anciennes créances avant que leur délai arrive à terme. En cas de qualification incertaine, faites examiner le contrat.

Avec un [logiciel de facturation suisse](/rechnungsprogramm), vous regroupez factures et rappels. Cette organisation facilite le suivi ; elle ne constitue pas une interruption juridique de la prescription.

Source : [Code des obligations, art. 127 à 135](https://www.fedlex.admin.ch/eli/cc/27/317_321_377/fr). Mise à jour : septembre 2026.""")
add(S,'it','Prescrizione delle fatture in Svizzera: termini',
"In Svizzera una fattura non si prescrive sempre dopo tre anni. Il termine ordinario è di dieci anni secondo l’art. 127 CO. Per i crediti elencati nell’art. 128 CO valgono termini più brevi. Il termine decorre dall’esigibilità del credito, come stabilisce l’art. 130 CO.",
[('Di regola 10 anni','L’art. 127 CO prevede dieci anni, salvo una disposizione speciale.'),('5 anni per determinati crediti','L’art. 128 CO comprende pigioni, interessi, salari, lavori artigianali e onorari di medici e avvocati.'),('Il sollecito non interrompe il termine','Nemmeno una raccomandata interrompe la prescrizione: gli atti rilevanti sono indicati nell’art. 135 CO.')],
"""## Quale termine si applica alla tua fattura?

Conta la natura del credito, non il nome del documento. Un incarico di progetto può rientrare nel termine ordinario di dieci anni, ma devi verificare le eccezioni. Fatturare ogni mese non determina, da solo, la classificazione giuridica del credito.

| Credito | Termine | Base legale |
|---|---|---|
| Credito senza termine speciale | 10 anni | Art. 127 CO |
| Pigioni e interessi periodici | 5 anni | Art. 128 n. 1 CO |
| Lavori artigianali, onorari medici o legali, salari | 5 anni | Art. 128 n. 3 CO |
| Credito attestato da un attestato di carenza di beni, verso il debitore | 20 anni | Art. 149a LEF |

## Da quando decorre il termine?

L’art. 130 CO fa decorrere la prescrizione dall’esigibilità. Conserva il contratto, le condizioni di pagamento accettate e la documentazione del lavoro svolto. La data della fattura può essere diversa da quella in cui il credito diventa esigibile.

**Esempio ipotetico:** emetti la fattura a luglio, con una scadenza concordata ad agosto. Il calcolo parte dall’esigibilità ad agosto; la durata dipende dal tipo di credito. Inviare un nuovo sollecito non sposta questa data.

## Come si interrompe la prescrizione?

L’art. 135 CO prevede il riconoscimento del debito da parte del debitore e determinati atti del creditore, tra cui una domanda di esecuzione, un’istanza di conciliazione o un’azione giudiziaria. Anche un pagamento parziale o di interessi può costituire un riconoscimento. Conserva le prove.

Un sollecito chiede il pagamento e può mettere in mora il debitore, ma **non interrompe la prescrizione**, nemmeno se fissa un nuovo termine. Il [modello di sollecito svizzero](/mahnung-vorlage-schweiz) ti aiuta a scrivere la richiesta; non sostituisce un atto interruttivo.

## Organizza i documenti

Riunisci contratto, fattura, prove della prestazione, scadenza, corrispondenza e pagamenti. Esamina i crediti più vecchi prima che il termine scada. Se la classificazione è dubbia, fai verificare il contratto.

Un [software di fatturazione svizzero](/rechnungsprogramm) ti aiuta a gestire fatture e solleciti. Il monitoraggio amministrativo non interrompe da solo la prescrizione.

Fonte: [Codice delle obbligazioni, art. 127–135](https://www.fedlex.admin.ch/eli/cc/27/317_321_377/it). Aggiornato a settembre 2026.""")
add(S,'en','Invoice limitation periods in Switzerland',
"Swiss invoices do not all become time-barred after three years. Article 127 of the Code of Obligations (CO) sets the ordinary period at ten years. Article 128 lists shorter periods. Article 130 governs when the clock starts: when the claim becomes due.",
[('Usually 10 years','Article 127 CO applies unless a special rule provides otherwise.'),('5 years for specified claims','Article 128 includes rent, interest, wages, craft work and doctors’ and lawyers’ fees.'),('A reminder does not stop the clock','Even a formal reminder does not interrupt limitation. Article 135 CO sets out the relevant acts.')],
"""## Which period applies?

The nature of the claim matters more than the document’s title. A project invoice may fall within the ordinary ten-year period, but check the exceptions. Monthly invoicing alone does not settle the legal classification.

| Claim | Period | Legal basis |
|---|---|---|
| Claim without a special period | 10 years | Art. 127 CO |
| Periodic rent and interest | 5 years | Art. 128 no. 1 CO |
| Craft work, medical or legal fees, wages | 5 years | Art. 128 no. 3 CO |
| Claim recorded in a certificate of loss, against the debtor | 20 years | Art. 149a DEBA |

## Start with the due date

Under Article 130 CO, limitation starts when the claim becomes due. Keep the contract, accepted payment terms and evidence of the work. The invoice issue date and due date may differ.

**Hypothetical example:** work is invoiced in July with an agreed August due date. Count from when the claim becomes due in August, using the period appropriate to the claim. Sending a reminder does not move that starting date.

## How can limitation be interrupted?

Article 135 CO covers acknowledgment by the debtor and specified creditor actions, including debt enforcement proceedings, a conciliation application or a court action. A partial payment or interest payment may also acknowledge the debt. Keep evidence of it.

A reminder requests payment and can place the debtor in default. It **does not interrupt limitation**, even if it sets a new deadline. A [Swiss payment reminder template](/mahnung-vorlage-schweiz) helps with the wording but cannot replace an interrupting legal act.

## Keep an enforceable paper trail

File the contract, invoice, evidence of delivery, due date, correspondence and payments together. Review older claims before their deadlines approach. If the classification is uncertain, have the contract assessed.

[Swiss invoicing software](/rechnungsprogramm) helps organise invoices and reminders. Administrative tracking itself does not interrupt the legal limitation period.

Source: [Code of Obligations, Articles 127–135](https://www.fedlex.admin.ch/eli/cc/27/317_321_377/en). Updated September 2026.""")
add(S,'es','Prescripción de facturas en Suiza: plazos',
"En Suiza, las facturas no prescriben siempre a los tres años. El art. 127 del Código de Obligaciones (CO) fija un plazo general de diez años. El art. 128 recoge plazos más cortos y el art. 130 establece el inicio del cómputo: cuando el crédito es exigible.",
[('10 años como regla general','El art. 127 CO se aplica salvo que exista una norma especial.'),('5 años en determinados casos','El art. 128 incluye alquileres, intereses, salarios, trabajos artesanales y honorarios médicos y de abogados.'),('Un recordatorio no interrumpe el plazo','Ni siquiera un requerimiento formal interrumpe la prescripción. Los actos pertinentes figuran en el art. 135 CO.')],
"""## Qué plazo corresponde a su factura

Importa la naturaleza del crédito, no el título del documento. Una factura por un proyecto puede estar sujeta al plazo general de diez años, pero hay que comprobar las excepciones. Facturar mensualmente no determina por sí solo la clasificación jurídica.

| Crédito | Plazo | Base legal |
|---|---|---|
| Crédito sin plazo especial | 10 años | Art. 127 CO |
| Alquileres e intereses periódicos | 5 años | Art. 128 ap. 1 CO |
| Trabajos artesanales, honorarios médicos o jurídicos, salarios | 5 años | Art. 128 ap. 3 CO |
| Crédito reconocido en un certificado de descubierto, frente al deudor | 20 años | Art. 149a LP |

## El cómputo empieza con la exigibilidad

El art. 130 CO sitúa el inicio en la exigibilidad del crédito. Conserve el contrato, las condiciones de pago aceptadas y la prueba del trabajo. La fecha de emisión puede ser distinta de la fecha de vencimiento.

**Ejemplo hipotético:** una factura se emite en julio con vencimiento acordado en agosto. Se cuenta desde la exigibilidad en agosto, aplicando el plazo correspondiente al crédito. Un nuevo recordatorio no desplaza esa fecha.

## Cómo interrumpir la prescripción

El art. 135 CO contempla el reconocimiento de deuda por el deudor y determinados actos del acreedor: procedimiento de ejecución, solicitud de conciliación o demanda judicial. Un pago parcial o de intereses también puede constituir reconocimiento. Conserve la prueba.

Un requerimiento reclama el pago y puede constituir al deudor en mora, pero **no interrumpe la prescripción**, aunque conceda otro plazo. La [plantilla de requerimiento suiza](/mahnung-vorlage-schweiz) facilita la redacción; no sustituye un acto interruptivo.

## Mantenga un expediente claro

Reúna contrato, factura, justificantes de la prestación, vencimiento, comunicaciones y pagos. Revise los créditos antiguos antes de que prescriban. Si hay dudas sobre su clasificación, solicite una revisión del contrato.

Un [software de facturación suizo](/rechnungsprogramm) ayuda a organizar facturas y recordatorios. Ese seguimiento administrativo no interrumpe por sí solo el plazo legal.

Fuente: [Código de Obligaciones, arts. 127–135, en francés](https://www.fedlex.admin.ch/eli/cc/27/317_321_377/fr). Actualizado en septiembre de 2026.""")
add(S,'pt','Prescrição de faturas na Suíça: prazos',
"Na Suíça, uma fatura não prescreve sempre ao fim de três anos. O art. 127 do Código das Obrigações (CO) fixa o prazo geral em dez anos. O art. 128 prevê prazos mais curtos e o art. 130 determina o início da contagem: quando o crédito se torna exigível.",
[('Regra geral: 10 anos','O art. 127 CO aplica-se quando não existe uma regra especial.'),('5 anos em casos específicos','O art. 128 inclui rendas, juros, salários, trabalhos artesanais e honorários médicos e de advogados.'),('Um lembrete não interrompe o prazo','Mesmo uma interpelação formal não interrompe a prescrição. Os atos relevantes constam do art. 135 CO.')],
"""## Qual é o prazo da sua fatura?

A natureza do crédito é mais importante do que o título do documento. Uma fatura de projeto pode ter o prazo geral de dez anos, mas é preciso verificar as exceções. A faturação mensal, por si só, não define a classificação jurídica.

| Crédito | Prazo | Base legal |
|---|---|---|
| Crédito sem prazo especial | 10 anos | Art. 127 CO |
| Rendas e juros periódicos | 5 anos | Art. 128 n.º 1 CO |
| Trabalhos artesanais, honorários médicos ou jurídicos, salários | 5 anos | Art. 128 n.º 3 CO |
| Crédito documentado por certificado de insuficiência de bens, contra o devedor | 20 anos | Art. 149a LP |

## A contagem começa na exigibilidade

O art. 130 CO estabelece que o prazo começa quando o crédito é exigível. Guarde o contrato, as condições de pagamento aceites e a prova do serviço. A data de emissão pode não coincidir com o vencimento.

**Exemplo hipotético:** uma fatura é emitida em julho com vencimento acordado em agosto. A contagem parte da exigibilidade em agosto e usa o prazo correspondente ao crédito. Um novo lembrete não altera essa data.

## Como interromper a prescrição

O art. 135 CO prevê o reconhecimento da dívida pelo devedor e certos atos do credor, como um pedido de execução, de conciliação ou uma ação judicial. Um pagamento parcial ou de juros também pode constituir reconhecimento. Guarde os comprovativos.

Uma interpelação solicita o pagamento e pode constituir o devedor em mora. Contudo, **não interrompe a prescrição**, mesmo com um novo prazo. O [modelo de interpelação suíço](/mahnung-vorlage-schweiz) ajuda a redigir o pedido, mas não substitui um ato interruptivo.

## Organize os documentos

Reúna contrato, fatura, prova da prestação, vencimento, correspondência e pagamentos. Reveja os créditos antigos antes de o prazo terminar. Se a classificação for incerta, peça uma análise do contrato.

Um [software de faturação suíço](/rechnungsprogramm) ajuda a acompanhar faturas e lembretes. A organização administrativa não interrompe, por si só, o prazo legal.

Fonte: [Código das Obrigações, arts. 127–135, em francês](https://www.fedlex.admin.ch/eli/cc/27/317_321_377/fr). Atualizado em setembro de 2026.""")
S='zahlungsfristen-schweiz'
add(S,'fr','Délais de paiement en Suisse : échéance et demeure',
"La Suisse ne connaît pas de délai légal général de paiement de 30 jours. Sans accord ni autre indication résultant de la nature de l’affaire, la dette est immédiatement exigible selon l’art. 75 CO. L’exigibilité et la demeure sont deux étapes distinctes.",
[('30 jours : un usage','Vous pouvez convenir de 30 jours nets, mais ce délai ne découle pas automatiquement de la loi.'),('Demeure avec ou sans rappel','Art. 102 al. 1 CO : un rappel est en principe nécessaire. Al. 2 : un terme convenu et déterminé permet la demeure automatique à son expiration.'),('Facture et TVA','Les indications requises pour la TVA relèvent de l’art. 26 LTVA (MWSTG), pas de l’art. 469 CO.')],
"""## Convenez du délai avant de facturer

Choisissez un délai adapté à la mission et faites-le accepter avec le devis ou le contrat. Vous pouvez proposer 14 ou 30 jours, un acompte ou des paiements par étapes. Ce sont des choix contractuels, pas des délais légaux universels.

Indiquez ensuite clairement l’échéance convenue sur la facture. Ajouter unilatéralement une date à une facture ne suffit pas à établir qu’un terme a été convenu au sens de l’art. 102 al. 2 CO.

## Quand commence la demeure ?

Sans terme convenu et déterminé, une interpellation du créancier est en principe nécessaire après l’exigibilité (art. 102 al. 1 CO). Si les parties ont convenu d’un terme déterminé, la demeure intervient à son expiration sans rappel (art. 102 al. 2 CO).

L’intérêt moratoire légal est en principe de **5% par an** dès la demeure (art. 104 CO). Il ne commence donc pas automatiquement 30 jours après réception de toute facture. Conservez la preuve du terme accepté ou de la réception du rappel.

**Exemple fictif :** pour CHF 1'250.00 en demeure pendant 30 jours, un calcul sur 365 jours donne CHF 1'250.00 × 5% × 30 / 365 = **CHF 5.14**.

## Que doit contenir la facture ?

Pour la TVA, l’art. 26 LTVA prévoit notamment l’identification du fournisseur et du destinataire, le numéro TVA du fournisseur, la nature, l’étendue et la date de la prestation, la contre-prestation et les indications fiscales nécessaires. Les taux suisses sont **8.1%, 2.6% et 3.8%**, selon la prestation. N’ajoutez pas de TVA si vous n’êtes pas autorisé à la facturer.

Une référence de facture et l’échéance facilitent le suivi. Le délai de paiement n’est pas une indication obligatoire au titre de l’art. 26 LTVA. Le [modèle de facture suisse](/rechnungsvorlage) vous aide à organiser ces informations.

Une QR-facture peut utiliser un IBAN ordinaire ou un QR-IBAN selon le type de référence. Le code QR ne remplace pas l’accord sur le paiement.

## Relance et poursuite

Vérifiez d’abord si le paiement a été reçu ou si une contestation reste ouverte. Envoyez ensuite une demande claire avec le montant, la référence et le délai de réponse. Utilisez le [modèle de rappel](/mahnung-vorlage-schweiz) et conservez les échanges.

Il n’existe pas de tarif légal général des frais de rappel. Supprimez les frais sans base vérifiable. En cas de poursuite, les frais dépendent du montant réclamé ; le créancier doit les avancer. Un rappel n’interrompt pas la prescription.

Le [logiciel de facturation Magic Heidi](/rechnungsprogramm) regroupe factures, dépenses et rappels. Le forfait gratuit comprend 3 factures et 3 dépenses. Pro coûte CHF 25.00 par mois avec facturation annuelle (CHF 299.00 par an), ou CHF 39.00 au mois : [tarifs](/pricing).

Source : [Code des obligations, art. 75 et 102–104](https://www.fedlex.admin.ch/eli/cc/27/317_321_377/fr). Mise à jour : septembre 2026.""",
[('Ai-je toujours 30 jours pour payer ?','Non. Le délai dépend de l’accord. Sans accord ou autre indication liée à l’affaire, la dette est immédiatement exigible selon l’art. 75 CO.'),('Une facture échue entraîne-t-elle toujours la demeure ?','Non. Un rappel est en principe nécessaire, sauf notamment lorsqu’un terme déterminé a été convenu (art. 102 CO).')])
add(S,'it','Termini di pagamento in Svizzera: scadenza e mora',
"In Svizzera non esiste un termine legale generale di pagamento di 30 giorni. In assenza di un accordo o di indicazioni derivanti dalla natura dell’affare, il debito è subito esigibile secondo l’art. 75 CO. Esigibilità e mora sono due momenti distinti.",
[('30 giorni: una consuetudine','Puoi concordare 30 giorni netti, ma non è un termine imposto automaticamente dalla legge.'),('Quando scatta la mora','Art. 102 cpv. 1 CO: di regola serve un’interpellazione. Cpv. 2: con una scadenza determinata e concordata, la mora scatta alla sua scadenza.'),('Indicazioni IVA','La norma pertinente è l’art. 26 LIVA (MWSTG), non l’art. 469 CO.')],
"""## Concorda il termine prima della fattura

Scegli un termine adatto all’incarico e fallo accettare con l’offerta o il contratto. Puoi proporre 14 o 30 giorni, un anticipo o pagamenti per fasi. Sono scelte contrattuali, non termini legali universali.

Riporta poi la scadenza concordata sulla fattura. Aggiungere unilateralmente una data non dimostra che le parti abbiano concordato un termine ai sensi dell’art. 102 cpv. 2 CO.

## Quando inizia la mora?

Senza una scadenza determinata e concordata, dopo l’esigibilità serve di regola un’interpellazione del creditore (art. 102 cpv. 1 CO). Se il termine è stato concordato, la mora interviene alla sua scadenza senza sollecito (art. 102 cpv. 2 CO).

L’interesse moratorio legale è di regola del **5% annuo** dalla mora (art. 104 CO). Non inizia automaticamente 30 giorni dopo la ricezione di qualsiasi fattura. Conserva la prova del termine accettato o della ricezione del sollecito.

**Esempio ipotetico:** su CHF 1'250.00 in mora per 30 giorni, usando un anno di 365 giorni: CHF 1'250.00 × 5% × 30 / 365 = **CHF 5.14**.

## Cosa deve contenere la fattura?

Per l’IVA, l’art. 26 LIVA prevede in particolare i dati di fornitore e destinatario, il numero IVA del fornitore, natura, entità e data della prestazione, controprestazione e indicazioni fiscali necessarie. Le aliquote svizzere sono **8.1%, 2.6% e 3.8%**, secondo la prestazione. Non addebitare IVA se non sei autorizzato a farlo.

Numero della fattura e scadenza aiutano il controllo. Il termine di pagamento non è un’indicazione obbligatoria ai sensi dell’art. 26 LIVA. Puoi organizzare i dati con il [modello di fattura svizzero](/rechnungsvorlage).

Una fattura QR può usare un IBAN ordinario o un QR-IBAN, a seconda del riferimento. Il codice QR non sostituisce l’accordo sul pagamento.

## Sollecito ed esecuzione

Verifica prima se il pagamento è arrivato o se resta una contestazione da chiarire. Invia poi una richiesta con importo, riferimento e termine di risposta. Usa il [modello di sollecito](/mahnung-vorlage-schweiz) e conserva la corrispondenza.

Non esiste una tariffa legale generale per le spese di sollecito. Elimina gli addebiti privi di una base verificabile. Le spese di esecuzione dipendono dall’importo richiesto e devono essere anticipate dal creditore. Un sollecito non interrompe la prescrizione.

Il [software di fatturazione Magic Heidi](/rechnungsprogramm) riunisce fatture, spese e solleciti. Il piano gratuito include 3 fatture e 3 spese. Pro costa CHF 25.00 al mese con pagamento annuale (CHF 299.00 all’anno), oppure CHF 39.00 con pagamento mensile: [prezzi](/pricing).

Fonte: [Codice delle obbligazioni, art. 75 e 102–104](https://www.fedlex.admin.ch/eli/cc/27/317_321_377/it). Aggiornato a settembre 2026.""",
[('Ho sempre 30 giorni per pagare?','No. Vale quanto concordato. Senza accordo o altre indicazioni legate all’affare, il debito è subito esigibile secondo l’art. 75 CO.'),('Una fattura scaduta comporta sempre la mora?','No. Di regola occorre un’interpellazione, salvo in particolare una scadenza determinata e concordata ai sensi dell’art. 102 CO.')])
add(S,'en','Swiss payment terms: due dates and default',
"Switzerland has no general statutory 30-day payment period. Without an agreement or a different conclusion from the nature of the transaction, payment is due immediately under Article 75 CO. A debt being due and a debtor being in default are separate matters.",
[('30 days is customary','Net 30 can be agreed, but it is not an automatic legal payment period.'),('Default needs the right trigger','Article 102(1) CO generally requires a reminder. Under Article 102(2), an agreed fixed deadline triggers default when it expires.'),('VAT invoice rules','Article 26 of the VAT Act (MWSTG), not Article 469 CO, governs the relevant VAT invoice information.')],
"""## Agree terms before invoicing

Choose terms appropriate to the work and obtain agreement with the quote or contract. You might propose 14 or 30 days, an advance payment or milestones. These are contractual choices, not universal legal deadlines.

Show the agreed due date clearly on the invoice. Unilaterally adding a date to an invoice does not establish an agreed deadline under Article 102(2) CO.

## When does default start?

Without an agreed fixed deadline, a creditor’s reminder is generally required after payment becomes due (Article 102(1)). Where the parties agreed a fixed deadline, default starts on its expiry without a reminder (Article 102(2)).

Statutory default interest is generally **5% a year** from default under Article 104 CO. It does not automatically start 30 days after every invoice arrives. Keep evidence of the accepted terms or receipt of the reminder.

**Hypothetical example:** for CHF 1'250.00 in default for 30 days, using a 365-day year: CHF 1'250.00 × 5% × 30 / 365 = **CHF 5.14**.

## Invoice details

For VAT purposes, Article 26 of the VAT Act covers supplier and recipient identification, the supplier’s VAT number, the nature, extent and date of the supply, consideration and the necessary tax information. Swiss VAT rates are **8.1%, 2.6% and 3.8%**, depending on the supply. Do not charge VAT unless entitled to do so.

An invoice reference and due date help with tracking. Payment terms are not mandatory particulars under Article 26. Use the [Swiss invoice template](/rechnungsvorlage) to organise the details.

A QR-bill can use a regular IBAN or QR-IBAN, depending on the reference type. The QR code does not replace agreed payment terms.

## Reminders and debt enforcement

Check whether payment has arrived or a dispute needs resolving. Then send a clear request stating the amount, reference and response deadline. Use a [payment reminder template](/mahnung-vorlage-schweiz) and retain correspondence.

There is no general statutory reminder-fee tariff. Remove charges without a verifiable basis. Debt enforcement fees depend on the claim amount and must be advanced by the creditor. A reminder does not interrupt limitation.

[Magic Heidi invoicing software](/rechnungsprogramm) brings together invoices, expenses and reminders. Free includes 3 invoices and 3 expenses. Pro is CHF 25.00 a month billed annually (CHF 299.00 a year), or CHF 39.00 billed monthly: [pricing](/pricing).

Source: [Code of Obligations, Articles 75 and 102–104](https://www.fedlex.admin.ch/eli/cc/27/317_321_377/en). Updated September 2026.""",
[('Do I always have 30 days to pay?','No. The agreement governs. Without agreed terms or a different conclusion from the transaction, payment is immediately due under Article 75 CO.'),('Does an overdue invoice always mean default?','No. A reminder is generally needed unless, in particular, the parties agreed a fixed deadline under Article 102 CO.')])
add(S,'es','Plazos de pago en Suiza: vencimiento y mora',
"Suiza no tiene un plazo legal general de pago de 30 días. Sin acuerdo ni otra indicación derivada de la naturaleza del negocio, la deuda es exigible inmediatamente según el art. 75 CO. La exigibilidad y la mora son cuestiones distintas.",
[('30 días: una costumbre','Puedes acordar 30 días netos, pero no es un plazo legal automático.'),('Cuándo empieza la mora','El art. 102.1 CO exige en general un requerimiento. El art. 102.2 permite la mora automática al vencer un plazo determinado y acordado.'),('Datos fiscales de la factura','La norma pertinente es el art. 26 de la ley del IVA (MWSTG), no el art. 469 CO.')],
"""## Acuerda las condiciones antes de facturar

Elige un plazo adecuado al encargo y obtén su aceptación con la oferta o el contrato. Puedes proponer 14 o 30 días, anticipos o pagos por etapas. Son opciones contractuales, no plazos legales universales.

Indica después el vencimiento acordado en la factura. Añadir unilateralmente una fecha no demuestra un acuerdo a efectos del art. 102.2 CO.

## Inicio de la mora e intereses

Sin un plazo determinado y acordado, generalmente hace falta un requerimiento del acreedor después de la exigibilidad (art. 102.1 CO). Si las partes acordaron un plazo determinado, la mora comienza al vencerlo sin requerimiento (art. 102.2 CO).

El interés legal de demora es, en general, del **5% anual** desde la mora (art. 104 CO). No empieza automáticamente 30 días después de recibir cualquier factura. Guarda la prueba de las condiciones aceptadas o de la recepción del requerimiento.

**Ejemplo hipotético:** CHF 1'250.00 en mora durante 30 días, con un año de 365 días: CHF 1'250.00 × 5% × 30 / 365 = **CHF 5.14**.

## Datos de la factura

El art. 26 MWSTG recoge la identificación del proveedor y destinatario, número de IVA del proveedor, naturaleza, alcance y fecha de la prestación, contraprestación y datos fiscales necesarios. Los tipos suizos son **8.1%, 2.6% y 3.8%**, según la prestación. No cobres IVA sin estar autorizado.

El número de factura y el vencimiento facilitan el seguimiento. El plazo de pago no es un dato obligatorio según el art. 26. Usa la [plantilla de factura suiza](/rechnungsvorlage) para organizar la información.

Una factura QR puede usar un IBAN ordinario o un QR-IBAN según el tipo de referencia. El código no sustituye el acuerdo sobre el pago.

## Requerimiento y ejecución

Comprueba primero si llegó el pago o hay una reclamación pendiente. Envía después una solicitud clara con importe, referencia y plazo de respuesta. Usa la [plantilla de requerimiento](/mahnung-vorlage-schweiz) y conserva los mensajes.

No existe una tarifa legal general de gastos de requerimiento. Elimina cargos sin una base verificable. Las tasas de ejecución dependen del importe reclamado y el acreedor debe adelantarlas. Un requerimiento no interrumpe la prescripción.

El [software de facturación Magic Heidi](/rechnungsprogramm) reúne facturas, gastos y recordatorios. El plan gratuito incluye 3 facturas y 3 gastos. Pro cuesta CHF 25.00 al mes con pago anual (CHF 299.00 al año), o CHF 39.00 con pago mensual: [precios](/pricing).

Fuente: [Código de Obligaciones, arts. 75 y 102–104, en francés](https://www.fedlex.admin.ch/eli/cc/27/317_321_377/fr). Actualizado en septiembre de 2026.""",
[('¿Siempre tengo 30 días para pagar?','No. Rige lo acordado. Sin acuerdo u otra indicación derivada del negocio, la deuda es exigible inmediatamente según el art. 75 CO.'),('¿Una factura vencida implica siempre mora?','No. Normalmente hace falta un requerimiento, salvo en particular un plazo determinado y acordado según el art. 102 CO.')])
add(S,'pt','Prazos de pagamento na Suíça: vencimento e mora',
"A Suíça não tem um prazo legal geral de pagamento de 30 dias. Sem acordo ou outra indicação decorrente da natureza do negócio, a dívida é imediatamente exigível segundo o art. 75 CO. Exigibilidade e mora são situações distintas.",
[('30 dias: um costume','É possível acordar 30 dias líquidos, mas não se trata de um prazo legal automático.'),('Quando começa a mora','O art. 102 n.º 1 CO exige geralmente uma interpelação. O n.º 2 permite a mora automática quando termina um prazo determinado e acordado.'),('Dados fiscais da fatura','A norma pertinente é o art. 26 da lei do IVA (MWSTG), não o art. 469 CO.')],
"""## Combine as condições antes de faturar

Escolha um prazo adequado ao trabalho e obtenha a aceitação na proposta ou no contrato. Pode propor 14 ou 30 dias, adiantamentos ou pagamentos por etapas. São opções contratuais, não prazos legais universais.

Indique depois o vencimento acordado na fatura. Acrescentar unilateralmente uma data não demonstra um acordo para efeitos do art. 102 n.º 2 CO.

## Início da mora e juros

Sem prazo determinado e acordado, é geralmente necessária uma interpelação do credor após a exigibilidade (art. 102 n.º 1 CO). Se as partes acordaram esse prazo, a mora começa quando termina, sem interpelação (art. 102 n.º 2 CO).

Os juros legais de mora são, em regra, de **5% ao ano** desde a mora (art. 104 CO). Não começam automaticamente 30 dias após a receção de qualquer fatura. Guarde a prova das condições aceites ou da receção da interpelação.

**Exemplo hipotético:** CHF 1'250.00 em mora durante 30 dias, num ano de 365 dias: CHF 1'250.00 × 5% × 30 / 365 = **CHF 5.14**.

## Dados da fatura

O art. 26 MWSTG prevê identificação do fornecedor e destinatário, número de IVA do fornecedor, natureza, extensão e data da prestação, contrapartida e dados fiscais necessários. As taxas suíças são **8.1%, 2.6% e 3.8%**, conforme a prestação. Não cobre IVA sem estar autorizado.

Número da fatura e vencimento ajudam no acompanhamento. O prazo de pagamento não é um dado obrigatório nos termos do art. 26. Use o [modelo de fatura suíço](/rechnungsvorlage) para organizar a informação.

Uma fatura QR pode usar um IBAN normal ou um QR-IBAN conforme a referência. O código não substitui o acordo sobre o pagamento.

## Interpelação e execução

Verifique primeiro se recebeu o pagamento ou existe uma reclamação por resolver. Envie depois um pedido claro com valor, referência e prazo de resposta. Use o [modelo de interpelação](/mahnung-vorlage-schweiz) e guarde a correspondência.

Não existe uma tabela legal geral de despesas de interpelação. Elimine encargos sem fundamento verificável. As taxas de execução dependem do valor reclamado e devem ser adiantadas pelo credor. Uma interpelação não interrompe a prescrição.

O [software de faturação Magic Heidi](/rechnungsprogramm) reúne faturas, despesas e lembretes. O plano gratuito inclui 3 faturas e 3 despesas. O Pro custa CHF 25.00 por mês com pagamento anual (CHF 299.00 por ano), ou CHF 39.00 com pagamento mensal: [preços](/pricing).

Fonte: [Código das Obrigações, arts. 75 e 102–104, em francês](https://www.fedlex.admin.ch/eli/cc/27/317_321_377/fr). Atualizado em setembro de 2026.""",
[('Tenho sempre 30 dias para pagar?','Não. Vale o acordo. Sem acordo ou outra indicação do negócio, a dívida é imediatamente exigível segundo o art. 75 CO.'),('Uma fatura vencida implica sempre mora?','Não. Geralmente é necessária uma interpelação, salvo nomeadamente um prazo determinado e acordado nos termos do art. 102 CO.')])
S='verrechnungssteuer-schweiz'
add(S,'fr','Impôt anticipé suisse : remboursement et formulaire 25',
"L’impôt anticipé suisse retient notamment 35% sur certains revenus de capitaux, comme les intérêts et dividendes de source suisse. Il ne s’agit pas du taux définitif de votre impôt sur le revenu. Le remboursement dépend de votre situation et du respect des conditions de déclaration.",
[('Particuliers : déclaration fiscale','Déclarez les revenus bruts et les montants retenus dans l’état des titres de votre déclaration cantonale.'),('Formulaire 25 : personnes morales','Les personnes morales ayant leur siège en Suisse demandent le remboursement de l’impôt anticipé suisse auprès de l’AFC avec le formulaire 25.'),('DA-1 : crédit d’impôt étranger','Pour les personnes physiques, le DA-1 sert à demander l’imputation des retenues étrangères admissibles sur intérêts et dividendes.')],
"""## Récupérer l’impôt anticipé suisse

Pour une personne physique, y compris l’exploitant d’une entreprise individuelle, la demande passe généralement par la déclaration fiscale cantonale. Reprenez le revenu **brut**, le montant retenu et les avoirs d’après les attestations bancaires. L’autorité vérifie le droit au remboursement ; le montant admis est imputé ou remboursé.

**Exemple purement illustratif :** sur CHF 1'000.00 d’intérêts soumis à l’impôt anticipé, la retenue de 35% est de CHF 350.00 et le versement net de CHF 650.00. Vous déclarez CHF 1'000.00, pas CHF 650.00. Si les conditions sont réunies, les CHF 350.00 sont remboursables ; l’imposition ordinaire du revenu reste distincte.

Le droit au remboursement s’éteint en principe trois ans après la fin de l’année civile au cours de laquelle la prestation était échue (art. 32 LIA). Conservez les attestations et vérifiez les années manquantes.

## À quoi sert le formulaire 25 ?

Le formulaire 25 concerne le remboursement de l’impôt anticipé suisse aux **personnes morales établies en Suisse**, notamment les SA et Sàrl. La demande est adressée à l’AFC, au plus tôt après la fin de l’année d’échéance. Ce n’est pas le formulaire de remboursement des retenues étrangères.

## Revenus étrangers : DA-1 et conventions fiscales

Une retenue sur un dividende étranger n’est pas l’impôt anticipé suisse. Pour une personne physique, le **DA-1** permet de demander l’imputation de la part admissible de l’impôt étranger sur l’impôt suisse, selon la convention applicable et les limites prévues. La part récupérable dans le pays d’origine suit une autre procédure.

Le DA-1 ne garantit donc pas le remboursement de toute retenue étrangère. Les personnes morales utilisent d’autres formulaires, notamment le DA-2 pour les intérêts et dividendes. Consultez les [formulaires et instructions de l’AFC](https://www.estv.admin.ch/de/formulare-wegleitungen-direkte-bundessteuer).

## Dividendes de votre propre société

Une distribution d’une SA ou Sàrl suisse peut entraîner une retenue de 35%. La société gère la retenue ; l’actionnaire déclare le dividende brut dans sa propre déclaration. Le formulaire 25 de la société ne remplace pas cette déclaration privée. L’imposition partielle éventuelle du dividende est une question distincte du remboursement.

## Erreurs à éviter

Ne confondez pas revenu net et brut, impôt suisse et retenue étrangère, ni demande de la société et déclaration de l’actionnaire. Une omission de revenu peut compromettre le remboursement ; les conséquences dépendent des circonstances et d’une éventuelle correction.

La TVA est une autre taxe : ses taux sont **8.1%, 2.6% et 3.8%**. Elle ne se compense pas directement avec l’impôt anticipé. Un [logiciel de comptabilité](/buchhaltungssoftware) aide à conserver les justificatifs, sans décider de votre droit au remboursement.

Sources : [AFC, formulaire 25](https://www.estv.admin.ch/de/formulare-rueckerstattung-verrechnungssteuer-wohnsitz-schweiz), [LIA](https://www.fedlex.admin.ch/eli/cc/1966/371_385_384/fr). Mise à jour : septembre 2026.""",
[('Le formulaire 25 rembourse-t-il les retenues étrangères ?','Non. Il concerne l’impôt anticipé suisse des personnes morales établies en Suisse. Pour les personnes physiques, le DA-1 vise l’imputation de retenues étrangères admissibles.'),('Dois-je déclarer le brut ou le net ?','Le revenu brut et la retenue selon l’attestation bancaire. Le remboursement admis et l’impôt ordinaire sur le revenu sont deux calculs distincts.')])
add(S,'it','Imposta preventiva svizzera: rimborso e modulo 25',
"L’imposta preventiva svizzera trattiene, tra l’altro, il 35% su determinati redditi da capitale, come interessi e dividendi di fonte svizzera. Non è l’aliquota definitiva dell’imposta sul reddito. Il rimborso dipende dalla tua situazione e dal rispetto degli obblighi di dichiarazione.",
[('Persone fisiche: dichiarazione fiscale','Dichiara redditi lordi e trattenute nell’elenco titoli della dichiarazione cantonale.'),('Modulo 25: persone giuridiche','Le persone giuridiche con sede in Svizzera chiedono all’AFC il rimborso dell’imposta preventiva svizzera tramite il modulo 25.'),('DA-1: imposte estere','Per le persone fisiche, il DA-1 serve a chiedere il computo delle ritenute estere ammissibili su interessi e dividendi.')],
"""## Recuperare l’imposta preventiva svizzera

Per una persona fisica, anche se titolare di una ditta individuale, la richiesta passa generalmente dalla dichiarazione fiscale cantonale. Riporta reddito **lordo**, trattenuta e patrimonio secondo le attestazioni bancarie. L’autorità verifica il diritto al rimborso; l’importo riconosciuto viene accreditato o rimborsato.

**Esempio illustrativo:** su CHF 1'000.00 di interessi soggetti all’imposta preventiva, la trattenuta del 35% è CHF 350.00 e il versamento netto CHF 650.00. Dichiari CHF 1'000.00, non CHF 650.00. Se i requisiti sono soddisfatti, i CHF 350.00 sono rimborsabili; l’imposta ordinaria sul reddito resta distinta.

Il diritto al rimborso si estingue di regola tre anni dopo la fine dell’anno civile in cui la prestazione è scaduta (art. 32 LIP). Conserva le attestazioni e verifica gli anni mancanti.

## A cosa serve il modulo 25?

Il modulo 25 riguarda il rimborso dell’imposta preventiva svizzera alle **persone giuridiche con sede in Svizzera**, tra cui SA e Sagl. Si presenta all’AFC, non prima della fine dell’anno di scadenza. Non è il modulo per recuperare ritenute estere.

## Redditi esteri: DA-1 e convenzioni fiscali

La ritenuta su un dividendo estero non è l’imposta preventiva svizzera. Per le persone fisiche, il **DA-1** permette di chiedere il computo della parte ammissibile dell’imposta estera nell’imposta svizzera, secondo la convenzione e i limiti applicabili. La quota recuperabile nel paese d’origine segue una procedura diversa.

Il DA-1 non garantisce quindi il rimborso integrale delle ritenute estere. Le persone giuridiche utilizzano altri moduli, tra cui il DA-2 per interessi e dividendi. Consulta i [moduli e le istruzioni dell’AFC](https://www.estv.admin.ch/de/formulare-wegleitungen-direkte-bundessteuer).

## Dividendi della tua società

Una distribuzione di una SA o Sagl svizzera può comportare una trattenuta del 35%. La società gestisce la trattenuta; l’azionista dichiara il dividendo lordo nella propria dichiarazione. Il modulo 25 della società non sostituisce la dichiarazione privata. L’eventuale imposizione parziale del dividendo è distinta dal rimborso.

## Errori da evitare

Non confondere netto e lordo, imposta svizzera e ritenuta estera, richiesta della società e dichiarazione dell’azionista. Omettere un reddito può compromettere il rimborso; le conseguenze dipendono dalle circostanze e dall’eventuale rettifica.

L’IVA è un’altra imposta, con aliquote **8.1%, 2.6% e 3.8%**. Non si compensa direttamente con l’imposta preventiva. Un [software di contabilità](/buchhaltungssoftware) ti aiuta a conservare i documenti, senza determinare il diritto al rimborso.

Fonti: [AFC, modulo 25](https://www.estv.admin.ch/de/formulare-rueckerstattung-verrechnungssteuer-wohnsitz-schweiz), [LIP](https://www.fedlex.admin.ch/eli/cc/1966/371_385_384/it). Aggiornato a settembre 2026.""",
[('Il modulo 25 rimborsa le ritenute estere?','No. Riguarda l’imposta preventiva svizzera delle persone giuridiche con sede in Svizzera. Per le persone fisiche, il DA-1 serve al computo delle ritenute estere ammissibili.'),('Devo dichiarare il lordo o il netto?','Il reddito lordo e la trattenuta indicati nell’attestazione bancaria. Rimborso riconosciuto e imposta ordinaria sul reddito sono calcoli distinti.')])
add(S,'en','Swiss withholding tax: refunds and Form 25',
"Swiss withholding tax deducts 35% from specified investment income, such as Swiss-source interest and dividends. This is not your final income tax rate. A refund depends on your circumstances and meeting the declaration requirements.",
[('Individuals: tax return','Declare gross income and tax withheld in the securities schedule of your cantonal return.'),('Form 25: legal entities','Swiss-resident legal entities apply to the FTA for a refund of Swiss withholding tax using Form 25.'),('DA-1: foreign tax credit','Individuals use DA-1 to request credit for eligible foreign withholding tax on interest and dividends.')],
"""## Recovering Swiss withholding tax

For an individual, including a sole proprietor, the application generally goes through the cantonal tax return. Report **gross** income, withholding and assets from the bank statements. The authority assesses eligibility and credits or refunds the accepted amount.

**Illustrative example:** CHF 1'000.00 of interest subject to withholding produces CHF 350.00 tax at 35% and CHF 650.00 net cash. Declare CHF 1'000.00, not CHF 650.00. If the requirements are met, CHF 350.00 is refundable; ordinary income tax is assessed separately.

The refund entitlement generally expires three years after the end of the calendar year in which the income became due (Article 32 of the Withholding Tax Act). Keep statements and check any missing years.

## What is Form 25 for?

Form 25 covers refunds of Swiss withholding tax for **legal entities resident in Switzerland**, including AG and GmbH companies. Apply to the FTA no earlier than the end of the year in which the income became due. This is not a foreign withholding tax refund form.

## Foreign income: DA-1 and tax treaties

Tax deducted from a foreign dividend is not Swiss withholding tax. An individual can use **DA-1** to request a Swiss tax credit for the eligible foreign tax under the applicable treaty and limits. Any portion reclaimable from the source country follows a separate process.

DA-1 therefore does not guarantee repayment of every foreign deduction. Legal entities use other forms, including DA-2 for interest and dividends. See the [FTA forms and guidance](https://www.estv.admin.ch/de/formulare-wegleitungen-direkte-bundessteuer).

## Dividends from your own company

A distribution by a Swiss AG or GmbH may involve 35% withholding. The company handles the withholding; the shareholder reports the gross dividend in their own return. A company’s Form 25 does not replace the shareholder’s personal declaration. Any partial taxation of dividends is separate from the withholding refund.

## Common mistakes

Do not mix up gross and net income, Swiss and foreign withholding, or the company’s application and the shareholder’s return. Omitting income can jeopardise a refund; the consequences depend on the circumstances and any correction.

VAT is a different tax, with rates of **8.1%, 2.6% and 3.8%**. It is not directly offset against withholding tax. [Bookkeeping software](/buchhaltungssoftware) helps retain supporting records but does not determine refund eligibility.

Sources: [FTA Form 25](https://www.estv.admin.ch/de/formulare-rueckerstattung-verrechnungssteuer-wohnsitz-schweiz), [Withholding Tax Act, French text](https://www.fedlex.admin.ch/eli/cc/1966/371_385_384/fr). Updated September 2026.""",
[('Does Form 25 recover foreign withholding tax?','No. It concerns Swiss withholding tax for Swiss-resident legal entities. Individuals use DA-1 to request credit for eligible foreign withholding.'),('Should I declare gross or net income?','Gross income and tax withheld as shown on the bank statement. The accepted refund and ordinary income tax are separate calculations.')])
add(S,'es','Impuesto anticipado suizo: reembolso y formulario 25',
"El impuesto anticipado suizo retiene un 35% sobre determinados rendimientos del capital, como intereses y dividendos de fuente suiza. No es el tipo definitivo del impuesto sobre la renta. El reembolso depende de su situación y del cumplimiento de las obligaciones de declaración.",
[('Personas físicas: declaración fiscal','Declare los ingresos brutos y las retenciones en la relación de valores de la declaración cantonal.'),('Formulario 25: personas jurídicas','Las personas jurídicas con sede en Suiza solicitan a la AFC el reembolso del impuesto anticipado suizo con el formulario 25.'),('DA-1: crédito por impuesto extranjero','Las personas físicas usan el DA-1 para solicitar la imputación de retenciones extranjeras admisibles sobre intereses y dividendos.')],
"""## Recuperar el impuesto anticipado suizo

Para una persona física, incluido el titular de una empresa individual, la solicitud suele tramitarse mediante la declaración fiscal cantonal. Declare el ingreso **bruto**, la retención y el patrimonio según los certificados bancarios. La autoridad comprueba el derecho y abona o reembolsa la cantidad aceptada.

**Ejemplo ilustrativo:** CHF 1'000.00 de intereses sujetos a retención generan CHF 350.00 de impuesto al 35% y CHF 650.00 netos. Se declaran CHF 1'000.00, no CHF 650.00. Si se cumplen las condiciones, los CHF 350.00 son reembolsables; el impuesto ordinario sobre la renta se calcula por separado.

El derecho al reembolso se extingue, en general, tres años después del final del año natural en que venció el rendimiento (art. 32 de la ley del impuesto anticipado). Conserve los certificados y revise los años pendientes.

## Para qué sirve el formulario 25

El formulario 25 corresponde al impuesto anticipado suizo de **personas jurídicas con sede en Suiza**, como SA y Sàrl. Se presenta a la AFC, como pronto después de finalizar el año del vencimiento. No es un formulario para recuperar retenciones extranjeras.

## Rendimientos extranjeros: DA-1 y convenios

La retención sobre un dividendo extranjero no es impuesto anticipado suizo. Una persona física puede usar el **DA-1** para solicitar un crédito fiscal suizo por la parte admisible del impuesto extranjero, según el convenio y los límites aplicables. La parte recuperable en el país de origen sigue otro procedimiento.

El DA-1 no garantiza el reembolso de toda retención extranjera. Las personas jurídicas usan otros formularios, como el DA-2 para intereses y dividendos. Consulte los [formularios e instrucciones de la AFC](https://www.estv.admin.ch/de/formulare-wegleitungen-direkte-bundessteuer).

## Dividendos de su propia sociedad

Una distribución de una sociedad suiza puede implicar una retención del 35%. La sociedad gestiona la retención y el accionista declara el dividendo bruto en su declaración privada. El formulario 25 de la sociedad no sustituye esa declaración. La posible tributación parcial del dividendo es una cuestión distinta.

## Errores frecuentes

No confunda bruto y neto, retención suiza y extranjera, ni solicitud de la sociedad y declaración del accionista. Omitir ingresos puede poner en riesgo el reembolso; las consecuencias dependen de las circunstancias y de una posible rectificación.

El IVA es otro impuesto, con tipos del **8.1%, 2.6% y 3.8%**. No se compensa directamente con el impuesto anticipado. Un [software de contabilidad](/buchhaltungssoftware) ayuda a conservar los justificantes, pero no determina el derecho al reembolso.

Fuentes: [AFC, formulario 25](https://www.estv.admin.ch/de/formulare-rueckerstattung-verrechnungssteuer-wohnsitz-schweiz), [ley del impuesto anticipado, en francés](https://www.fedlex.admin.ch/eli/cc/1966/371_385_384/fr). Actualizado en septiembre de 2026.""",
[('¿El formulario 25 recupera retenciones extranjeras?','No. Se refiere al impuesto anticipado suizo de personas jurídicas con sede en Suiza. Para personas físicas, el DA-1 solicita la imputación de retenciones extranjeras admisibles.'),('¿Debo declarar el bruto o el neto?','El ingreso bruto y la retención del certificado bancario. El reembolso aceptado y el impuesto ordinario sobre la renta se calculan por separado.')])
add(S,'pt','Imposto antecipado suíço: reembolso e formulário 25',
"O imposto antecipado suíço retém 35% sobre determinados rendimentos de capitais, como juros e dividendos de fonte suíça. Não é a taxa definitiva do imposto sobre o rendimento. O reembolso depende da sua situação e do cumprimento das obrigações declarativas.",
[('Pessoas singulares: declaração fiscal','Declare os rendimentos brutos e as retenções na lista de títulos da declaração cantonal.'),('Formulário 25: pessoas coletivas','As pessoas coletivas com sede na Suíça pedem à AFC o reembolso do imposto antecipado suíço através do formulário 25.'),('DA-1: crédito de imposto estrangeiro','As pessoas singulares usam o DA-1 para pedir a imputação de retenções estrangeiras elegíveis sobre juros e dividendos.')],
"""## Recuperar o imposto antecipado suíço

Para uma pessoa singular, incluindo o titular de uma empresa individual, o pedido passa geralmente pela declaração fiscal cantonal. Declare rendimento **bruto**, retenção e património conforme os comprovativos bancários. A autoridade verifica o direito e credita ou reembolsa o valor aceite.

**Exemplo ilustrativo:** CHF 1'000.00 de juros sujeitos a retenção originam CHF 350.00 de imposto a 35% e CHF 650.00 líquidos. Declaram-se CHF 1'000.00, não CHF 650.00. Se os requisitos forem cumpridos, os CHF 350.00 são reembolsáveis; o imposto ordinário sobre o rendimento é calculado separadamente.

O direito ao reembolso extingue-se, em regra, três anos após o fim do ano civil em que o rendimento se venceu (art. 32 da lei do imposto antecipado). Guarde os comprovativos e verifique anos em falta.

## Para que serve o formulário 25?

O formulário 25 destina-se ao imposto antecipado suíço das **pessoas coletivas com sede na Suíça**, incluindo sociedades anónimas e por quotas. É entregue à AFC, apenas após o fim do ano do vencimento. Não é o formulário para recuperar retenções estrangeiras.

## Rendimentos estrangeiros: DA-1 e convenções

A retenção sobre um dividendo estrangeiro não é imposto antecipado suíço. Uma pessoa singular pode usar o **DA-1** para pedir um crédito fiscal suíço pela parcela elegível do imposto estrangeiro, segundo a convenção e os limites aplicáveis. A parcela recuperável no país de origem segue outro procedimento.

O DA-1 não garante o reembolso de toda a retenção estrangeira. As pessoas coletivas usam outros formulários, como o DA-2 para juros e dividendos. Consulte os [formulários e instruções da AFC](https://www.estv.admin.ch/de/formulare-wegleitungen-direkte-bundessteuer).

## Dividendos da sua sociedade

Uma distribuição de uma sociedade suíça pode implicar retenção de 35%. A sociedade trata da retenção e o acionista declara o dividendo bruto na declaração pessoal. O formulário 25 da sociedade não substitui essa declaração. A eventual tributação parcial do dividendo é uma questão distinta.

## Erros a evitar

Não confunda bruto e líquido, retenção suíça e estrangeira, nem pedido da sociedade e declaração do acionista. Omitir rendimentos pode comprometer o reembolso; as consequências dependem das circunstâncias e de uma eventual correção.

O IVA é outro imposto, com taxas de **8.1%, 2.6% e 3.8%**. Não é compensado diretamente com o imposto antecipado. Um [software de contabilidade](/buchhaltungssoftware) ajuda a guardar comprovativos, sem determinar o direito ao reembolso.

Fontes: [AFC, formulário 25](https://www.estv.admin.ch/de/formulare-rueckerstattung-verrechnungssteuer-wohnsitz-schweiz), [lei do imposto antecipado, em francês](https://www.fedlex.admin.ch/eli/cc/1966/371_385_384/fr). Atualizado em setembro de 2026.""",
[('O formulário 25 recupera retenções estrangeiras?','Não. Refere-se ao imposto antecipado suíço de pessoas coletivas com sede na Suíça. Para pessoas singulares, o DA-1 pede a imputação de retenções estrangeiras elegíveis.'),('Devo declarar o bruto ou o líquido?','O rendimento bruto e a retenção do comprovativo bancário. O reembolso aceite e o imposto ordinário sobre o rendimento são cálculos distintos.')])
def render_task1():
 paths=[]
 for (slug,locale),(title,intro,takeaways,body,faq) in DATA.items():
  path=ROOT/f'content/{locale}/blog/{slug}.md'
  old=path.read_text()
  # Keep locale-specific author/date and hero asset; replace misleading metadata.
  prefix=old[:old.index('  ::markdown')]
  desc=intro.split('. ')[0]+'.'
  if len(desc)>160: desc=takeaways[0][1]+' '+takeaways[1][1]
  if len(desc)>160: desc=takeaways[0][1]
  prefix=re.sub(r'^(title|subtitle|description):.*$',lambda m:m.group(1)+': '+Q(title if m.group(1)=='title' else desc),prefix,flags=re.M)
  prefix=re.sub(r'^(  alt|label):.*$',lambda m:m.group(1)+': '+Q(title),prefix,flags=re.M)
  grid='  ::feature-grid\n  ---\n  id: key-takeaways\n  theme: elevated\n  item-width: 280px\n  items:\n'
  for t,d in takeaways:grid+=f'    - title: {Q(t)}\n      description: {Q(d)}\n      icon: "✓"\n'
  grid+='  ---\n  ::\n'
  md=lambda s:'  ::markdown\n  ---\n  as: article\n  ---\n'+''.join('  '+line+'\n' if line else '\n' for line in s.splitlines())
  result=prefix+md(intro)+'  ::\n\n'+grid+'\n'+md(body)
  if faq:
   result+='\n  ::pages-landing-faq\n  ---\n  label: FAQ\n  title: '+Q(title)+'\n  items:\n'
   for q,a in faq:result+=f'    - question: {Q(q)}\n      answer: {Q(a)}\n'
   result+='  ---\n  ::\n'
  result+='  ::\n\n::\n'
  path.write_text(result);paths.append(str(path))
 return paths
if __name__=='__main__':
 paths=render_task1()
 Path('/tmp/locale-parity/task1-files.txt').write_text('\n'.join(paths))
 subprocess.run(['/Users/nathanganser/Documents/Development/seomachine/venv/bin/python3','/Users/nathanganser/Documents/Development/seomachine/templates/validate_mdc.py',*paths],check=True)

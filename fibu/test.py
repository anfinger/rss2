# -*- coding: utf8 -*-

#0-10	GVC
#10-20	Primanotennummer
#21-30	Verwendungszweck
#31	Bankkennung (Auftraggeber /Zahlungsempf.)
#32	Kto.Nr. (Auftraggeber / Zahlungsempf.)
#33-34	Name (Auftraggeber / Zahlungsempf.)
#35-60	Textschlüsselergänzung
#61-64	Verwendungszweckprint

#EREF (Ende-zu-Ende Referenz) oder KREF (Kundenreferenz)
#MREF (Mandatsreferenz, nur bei Lastschriften)
#CRED (Creditor-ID) oder DEBT (Debitor-ID)
#ABWA (abweichender Auftraggeber)
#SVWZ (Verwendungszweckinformationen)

#835 Kontoschließung
#105 SEPA Basislastschrift

import os
import re
from mt940 import MT940
import csv
import decimal

#data = MT940('D:/users/Reiseservice/===DELATAPLANEXPORTE/STARMONEY/2016-01-04/mt940/STA_315080200EUR_13070024_EUR_20160226_144738.sta')
#data = MT940('C:/Users/af/Downloads/20160313-401062147-umsMT940.TXT')
#data = MT940('C:/Users/af/Downloads/test_mt940_privat.TXT')
data = MT940('D:/users/Reiseservice/===DELATAPLANEXPORTE/STARMONEY/2016-03-14/STA_315080200EUR_13070024_EUR_20160315_175542.sta')
#data = MT940('D:/users/Reiseservice/===DELATAPLANEXPORTE/STARMONEY/2016-02/STA_315080200EUR_13070024_EUR_20160315_134702.sta')
#texte = [stm[7] for stm in data.statements[0][4]]
#print('statements:')
#print(data.statements)
print '========================================================================'
print '========================================================================'
print 'Auftragsreferenz-Nr.:', data.statements[0][0]
print 'Kontobezeichnung:', data.statements[0][1]
print 'Auszugsnummer:', data.statements[0][2]
print 'Buchungsdatum:', data.statements[0][3][0]
print 'Betrag:', data.statements[0][3][1]
print 'Währung :', data.statements[0][3][2]
print '??? :', data.statements[0][5][0]
print '??? :', data.statements[0][5][1]
print '??? :', data.statements[0][5][2]
print '??? :', data.statements[0][6]
print '========================================================================'
print '========================================================================'

with open('D:/users/Reiseservice/===DELATAPLANEXPORTE/STARMONEY/2016-03-11/test.csv', 'wb') as csvfile:
    fibuwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_csv = []
    i = 0
    for stm in data.statements[0][4]:
        print stm
        print '(', i, ')'
        print 'Wertdatum:', stm[0]
        print 'Buchungsdatum:', stm[1]
        print 'Betrag:', stm[2]
        print 'Buchungsschlüssel:', stm[3]
        print 'Referenz:', stm[4]
        print 'Bankreferenz:', stm[5]
        print 'Zusatzdaten:', stm[6]
        codes = re.findall('\?\d{2}',re.sub('\n','',stm[7]))
        codes.insert(0,'Geschäftsvorfall')
        tmp = re.sub('\n','',stm[7])
        #tmp = re.sub('SVWZ\+','Verwendungszweckinformationen: ',tmp)
        #tmp = re.sub('SVWZ\+','',tmp)
        tmp = re.split('\?\d{2}',tmp)
        data_splitted = tmp
        data_splitted_new = []
        for k in range(0, len(data_splitted)):
            if data_splitted[0] == '166':
                data_splitted[0] = 'SEPA-Gutschrift (Einzelbuchung)'
            elif data_splitted[0] == '105':
                data_splitted[0] = 'SEPA Basislastschrift'
            elif data_splitted[0] == '192':
                data_splitted[0] = 'SEPA-Basislastschrift Eingang vorbehalten (Core, Sammler)'
            elif data_splitted[0] == '835':
                data_splitted[0] = 'Kontoschließung'
            elif data_splitted[0] == '191':
                data_splitted[0] = 'SEPA-Überweisungsdatei (Sammler)'
            elif data_splitted[0] == '006':
                data_splitted[0] = 'Kreditkartenabrechnung'
            elif data_splitted[0] == '004':
                data_splitted[0] = 'Abbuchung'
            elif data_splitted[0] == '005':
                data_splitted[0] = 'Lastschrift'
            elif data_splitted[0] == '116':
                data_splitted[0] = 'SEPA-Überweisung (Einzelbuchung)'
            if k > 0:
                codes_tmp = int(codes[k][1:3])
            else:
                codes_tmp = 1000 #codes[k][1:3]
            if codes_tmp < 10:
                codes[k] = 'Geschäftsvorfall'
                if codes[k-1] == 'Geschäftsvorfall':
                    data_splitted[k] = data_splitted[k-1] + ' ' + data_splitted[k]
                    data_splitted[k-1] = ''
                    codes[k-1] = ''
            elif codes_tmp < 20:
                codes[k] = 'Primanotennummer'
                if codes[k-1] == 'Primanotennummer':
                    data_splitted[k] = data_splitted[k-1] + ' ' + data_splitted[k]
                    data_splitted[k-1] = ''
                    codes[k-1] = ''
            elif codes_tmp < 30:
                if data_splitted[k][0:5] == 'EREF+':
                    codes[k] = 'Ende-zu-Ende Referenz'
                    data_splitted[k] = re.sub('EREF\+','',data_splitted[k])
                elif data_splitted[k][0:5] == 'KREF+':
                    codes[k] = 'Kundenreferenz'
                    data_splitted[k] = re.sub('KREF\+','',data_splitted[k])
                elif data_splitted[k][0:5] == 'MREF+':
                    codes[k] = 'Mandatsreferenz (Nur bei Lastschriften)'
                    data_splitted[k] = re.sub('MREF\+','',data_splitted[k])
                elif data_splitted[k][0:5] == 'CRED+':
                    codes[k] = 'Creditor-ID'
                    data_splitted[k] = re.sub('CRED\+','',data_splitted[k])
                elif data_splitted[k][0:5] == 'SVWZ+':
                    codes[k] = 'Verwendungszweck'
                    data_splitted[k] = re.sub('SVWZ\+','',data_splitted[k])
                elif data_splitted[k][0:5] == 'ABWA+':
                    codes[k] = 'abweichender Auftraggeber'
                    data_splitted[k] = re.sub('ABWA\+','',data_splitted[k])
                elif (codes[k-1] != 'Geschäftsvorfall') & (codes[k-1] != 'Primanotennummer'):
                    data_splitted[k] = data_splitted[k-1] + data_splitted[k]
                    codes[k] = codes[k-1]
                    data_splitted[k-1] = ''
                    codes[k-1] = ''
                else:
                    codes[k] = 'Verwendungszweck'
            elif codes_tmp < 31:
                codes[k] = 'Bankkennung (Auftraggeber /Zahlungsempf.)'
            elif codes_tmp < 32:
                codes[k] = 'Kto.Nr. (Auftraggeber /Zahlungsempf.)'
            elif codes_tmp < 34:
                codes[k] = 'Name (Auftraggeber /Zahlungsempf.)'
                if codes[k-1] == 'Name (Auftraggeber /Zahlungsempf.)':
                    data_splitted[k] = data_splitted[k-1] + data_splitted[k]
                    data_splitted[k-1] = ''
                    codes[k-1] = ''
            elif codes_tmp < 35:
                codes[k] = 'Textschlüsselergänzung'
        data_csv_tmp = ['','','','','','','','','','','','']
        data_csv_tmp[0] = i+1
        data_csv_tmp[1] = stm[0]
        data_csv_tmp[2] = stm[1]
        data_csv_tmp[3] = stm[2]
        for k in range(0, len(data_splitted)):
            if codes[k] != '':
                print codes[k], ' : ', data_splitted[k]
            if codes[k] == 'Geschäftsvorfall':
                data_csv_tmp[4] = data_splitted[k]
            if codes[k] == 'Name (Auftraggeber /Zahlungsempf.)':
                data_csv_tmp[5] = data_csv_tmp[5] + data_splitted[k]
            if codes[k] == 'abweichender Auftraggeber':
                data_csv_tmp[5] = data_csv_tmp[5] + ' ('+ data_splitted[k] + ') '
            if codes[k] == 'Verwendungszweck':
                data_csv_tmp[6] = data_splitted[k]
            if codes[k] == 'Ende-zu-Ende Referenz':
                data_csv_tmp[7] = data_splitted[k]
            if codes[k] == 'Kundenreferenz':
                data_csv_tmp[8] = data_splitted[k]
            if codes[k] == 'Mandatsreferenz (Nur bei Lastschriften)':
                data_csv_tmp[9] = data_splitted[k]
            if codes[k] == 'Creditor-ID':
                data_csv_tmp[10] = data_splitted[k]
        print('=============================================')
        data_csv.append(data_csv_tmp)
        fibuwriter.writerow(data_csv_tmp)
        i = i + 1

with open('D:/users/Reiseservice/===DELATAPLANEXPORTE/STARMONEY/2016-03-14/mt940.csv', 'wb') as csvfile:
    agendawriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    agendawriter.writerow(['Start-Saldo', data.statements[0][3][0], data.statements[0][3][1], data.statements[0][3][2]])
    agendawriter.writerow(['End-Saldo', data.statements[0][5][0], data.statements[0][5][1], data.statements[0][5][2]])

    saldo_tmp = decimal.Decimal(0)
    i = 0
    for bank_transaction in data_csv:
        data_csv_tmp = ['','','','','','','','','','','','','']
        data_csv_tmp[0] = ('%.2f' % abs(bank_transaction[3])).replace('.', ',')
        if bank_transaction[3] < 0:
            data_csv_tmp[1] = '-'
        else:
            data_csv_tmp[1] = '+'
        saldo_tmp = saldo_tmp + bank_transaction[3]
        data_csv_tmp[2] = ('%.2f' % (data.statements[0][3][1] + saldo_tmp)).replace('.', ',')
        if re.search("Deutsche", bank_transaction[6]):
            data_csv_tmp[3] = 16500
        elif re.search("/2016/R2", bank_transaction[6]):
            data_csv_tmp[3] = 36320
        elif re.search("/2016/2", bank_transaction[6]):
            data_csv_tmp[3] = 36320
        elif re.search("/2016/R1", bank_transaction[6]):
            data_csv_tmp[3] = 36300
        elif re.search("/2016/1", bank_transaction[6]):
            data_csv_tmp[3] = 36300
        else:
            data_csv_tmp[3] = 'FiBu-Konto'
        data_csv_tmp[4] = bank_transaction[6]
        data_csv_tmp[5] = i+1
        data_csv_tmp[6] = bank_transaction[2].strftime("%d%m%Y")
        data_csv_tmp[7] = '18000'
        data_csv_tmp[9] = 'bank'
        data_csv_tmp[12] = bank_transaction[5]
        agendawriter.writerow(data_csv_tmp)
        i = i + 1

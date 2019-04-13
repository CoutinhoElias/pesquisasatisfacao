--PREENCHE ABA COMPLEMENTO
INSERT INTO WFISCAL.sisifm00006 (idnotafiscal, idsituacao, idoperacao, idcondparticipante, idnrseguranca)
(SELECT cdnota, 'G7DCA080F3A3008C0FA2A7D1874D602' AS IDSITUACAO_1,
                 'G7DCA080F2F1F29F0D1F0E9E6C49106' AS IDOPERACAO_2,
                 'G7DCA080F303A2130D71ACC9AC4910C' AS IDCONDPARTICIPANTE_3,
                 'G7DCA080F382135C0F22FD7ADC49116' AS IDNRSEGURANCA_4
  FROM WFISCAL.M00006
  WHERE dtescrituracao >='01-09-2013' AND
        dtescrituracao <='30-09-2013' AND
        nmespecie='CF')


--DELETA COMPLEMENTO DOS CUPONS
delete from WFISCAL.sisifm00006 WHERE idnotafiscal IN(
SELECT cdnota FROM WFISCAL.M00006 WHERE dtescrituracao >='01-09-2013' AND dtescrituracao <='30-09-2013' AND nmespecie='CF')



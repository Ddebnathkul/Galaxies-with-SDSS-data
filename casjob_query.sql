Select
  galaxy.objID, petroR50_g AS R50_g, petroR50_u AS R50_u, petroR50_r AS R50_r, petroR50_i AS R50_i, petroR50_z AS R50_z,  galaxy.g, galaxy.r, specObj.z, 
  p.absMagR AS Mr into mydb.MyTable_1_Dwaipayan from galaxy, specObj, Photoz p, plateX
where
  galaxy.objID=specObj.bestObjID AND
  galaxy.objID = p.objID AND
  galaxy.objID <> 0 AND 
  specObj.plateID=plateX.plateID AND
  specObj.class='galaxy' AND
  specObj.z BETWEEN 0 AND 0.05 AND
  specObj.zWarning = 0 AND
ORDER BY
  specObj.z

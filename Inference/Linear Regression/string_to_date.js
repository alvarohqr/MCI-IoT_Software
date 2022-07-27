//Cambio de la fecha de string a date
db.Szeged_copy.updateMany(

  {},

  [{ "$set": { "Formatted Date": { "$toDate": "$Formatted Date" } }}]

);
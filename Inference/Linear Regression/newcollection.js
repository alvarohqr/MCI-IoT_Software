//Los elementos de la fecha se separan en distintos objetos (para un 
//posterior filtrado), se seleccionan los parametros de temperatura (s) 
//y humedad y finalmente se almacenan en una nueva colección (Clima).
db.Szeged_copy.aggregate(
   [
     {
       $project:
         {
           year: { $year: "$Formatted Date" },
           month: { $month: "$Formatted Date" },
           day: { $dayOfMonth: "$Formatted Date" },
           hour: { $hour: "$Formatted Date" },
           Temperature: "$Temperature (C)",
           ApparentTemperature: "$Apparent Temperature (C)",
           Humidity: "$Humidity"
         }
     },

     { $out : "Clima" }
   ]
)
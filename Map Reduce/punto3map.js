 var map3 = function() {
     var key = this.scores[0].type;
     var value = { count: 1, sum_scores: this.scores[0].score };

     emit(key, value);
    
};
var reduce3 = function(type, countObjVals) {
   reducedVal = { count: 0, sum_scores: 0 };

   for (var idx = 0; idx < countObjVals.length; idx++) {
       reducedVal.count += countObjVals[idx].count;
       reducedVal.sum_scores += countObjVals[idx].sum_scores;
   }

   return reducedVal;
};
var finalizeFunction2 = function (key, reducedVal) {
  reducedVal.avg = reducedVal.sum_scores/reducedVal.count;
  return reducedVal;
};
db.students.mapReduce(
   map3,
   reduce3,
   {
     out: { merge: "avg3" }, 
     finalize: finalizeFunction2
   }
 );
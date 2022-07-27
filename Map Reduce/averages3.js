 var mapFunction2 = function() {
    for (var idx = 0; idx < this.scores.length; idx++) {
       var key = this.scores[idx].type;
       var value = { count: 1, sum_scores: this.scores[idx].score };

       emit(key, value);
    }
};
var reduceFunction2 = function(type, countObjVals) {
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
   mapFunction2,
   reduceFunction2,
   {
     out: { merge: "avgs" }, 
     finalize: finalizeFunction2
   }
 );
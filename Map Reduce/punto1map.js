var map1 = function() {
    emit(this._id,this.scores);    
    };

var reducef1 = function(studentid,scores){
    var calif = scores[0];
    var aux = 0;
    for(var idx=0; idx<calif.length; idx++){
        aux = aux + calif[idx].score; 
        }
    var avg = aux/calif.length;
        return avg;
    };
db.students.mapReduce(map1, reducef1, 
    {
        out: "avg1"
        }
        )







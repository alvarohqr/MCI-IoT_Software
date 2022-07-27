var map2 = function() {
    emit(this._id,this.scores);    
    };

var reducef2 = function(studentid,scores){
    var calif = scores[0];
    var aux = 0;
    var avg = (calif[0].score + calif[2].score)/2;
        return avg;
    };
db.students.mapReduce(map2, reducef2, 
    {
        out: "avg2"
        }
        )
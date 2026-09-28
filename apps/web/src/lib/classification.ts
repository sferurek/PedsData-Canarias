export type ClassificationMethod="quantile"|"equal_interval"|"jenks"|"fixed_thresholds"|"categorical";
export function classificationBreaks(values:number[],method:ClassificationMethod,classes=4,fixed:number[]=[]){
 if(method==="fixed_thresholds")return fixed;
 const sorted=values.filter(Number.isFinite).sort((a,b)=>a-b);
 if(!sorted.length)return [];
 if(method==="equal_interval"){
  const min=sorted[0],max=sorted.at(-1)!;return Array.from({length:classes-1},(_,index)=>min+(max-min)*(index+1)/classes);
 }
 if(method==="quantile")return Array.from({length:classes-1},(_,index)=>sorted[Math.min(sorted.length-1,Math.ceil(sorted.length*(index+1)/classes)-1)]);
 if(method==="jenks"){
  const n=sorted.length,k=Math.min(classes,n),lower=Array.from({length:n+1},()=>Array(k+1).fill(0)),variance=Array.from({length:n+1},()=>Array(k+1).fill(Infinity));
  for(let i=1;i<=k;i++){lower[1][i]=1;variance[1][i]=0}
  for(let l=2;l<=n;l++){
   let sum=0,sumSquares=0,count=0;
   for(let m=1;m<=l;m++){
    const lowerIndex=l-m+1,value=sorted[lowerIndex-1];count++;sum+=value;sumSquares+=value*value;const current=sumSquares-sum*sum/count;
    if(lowerIndex!==1)for(let j=2;j<=k;j++)if(variance[l][j]>=current+variance[lowerIndex-1][j-1]){lower[l][j]=lowerIndex;variance[l][j]=current+variance[lowerIndex-1][j-1]}
   }
   lower[l][1]=1;variance[l][1]=sumSquares-sum*sum/count;
  }
  const breaks=Array(k+1).fill(0);breaks[k]=sorted.at(-1)!;breaks[0]=sorted[0];let count=k,index=n;
  while(count>1){const id=Math.max(0,Math.round(lower[index][count])-2);breaks[count-1]=sorted[id];index=Math.round(lower[index][count]-1);count--}
  return breaks.slice(1,-1);
 }
 return [];
}
export function stepExpression(property:string,breaks:number[],colors:string[]){
 const expression:(string|number|unknown[])[]=["step",["coalesce",["get",property],-Infinity],colors[0]];
 breaks.forEach((item,index)=>expression.push(item,colors[index+1]));
 return expression;
}

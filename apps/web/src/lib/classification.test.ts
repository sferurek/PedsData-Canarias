import {describe,expect,it} from "vitest";
import {classificationBreaks} from "./classification";
describe("cartographic classification",()=>{
 it("computes quantiles",()=>expect(classificationBreaks([1,2,3,4,5,6,7,8],"quantile",4)).toEqual([2,4,6]));
 it("computes equal intervals",()=>expect(classificationBreaks([0,40],"equal_interval",4)).toEqual([10,20,30]));
 it("keeps fixed thresholds",()=>expect(classificationBreaks([1,9],"fixed_thresholds",4,[5,10,15])).toEqual([5,10,15]));
 it("computes ordered Jenks breaks",()=>{const result=classificationBreaks([1,2,2,3,20,21,22,50],"jenks",3);expect(result).toHaveLength(2);expect(result[0]).toBeLessThanOrEqual(result[1])});
});

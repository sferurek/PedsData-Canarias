import {render,screen,fireEvent} from "@testing-library/react";
import {describe,it,expect} from "vitest";
import {UtilizationExplorer,formatUtilization} from "./UtilizationExplorer";
import {AdolescenceExplorer} from "./AdolescenceExplorer";
describe("phase6 admission boundaries",()=>{
 it("distinguishes null and zero",()=>{expect(formatUtilization(null)).toBe("No disponible");expect(formatUtilization(0)).toBe("0");});
 it("shows seven islands and missing teleconsultation",()=>{render(<UtilizationExplorer/>);expect(screen.getByLabelText("Isla SIAP").querySelectorAll("option")).toHaveLength(7);fireEvent.change(screen.getByLabelText("Año SIAP"),{target:{value:"2007"}});fireEvent.change(screen.getByLabelText("Lugar de consulta"),{target:{value:"TELECONSULTA"}});expect(screen.getByTestId("siap-value")).toHaveTextContent("No disponible");expect(screen.getByText(/Publicación insular en HOLD/)).toBeInTheDocument();});
 it("does not turn survey estimates into administrative prevalence",()=>{render(<AdolescenceExplorer/>);expect(screen.getByText(/SURVEY_ESTIMATE/)).toBeInTheDocument();expect(screen.getByText("17–18 años")).toBeInTheDocument();expect(screen.getAllByText("No publicado")).toHaveLength(5);});
});
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AccessGapTable } from "./AccessGapTable";
import { DataBadge } from "./DataBadge";
import { MapLegend, legendItems } from "./MapLegend";
import { Metric } from "./Metric";
import { SourceMethodPanel } from "./SourceMethodPanel";
import { profiles } from "@/lib/data";

describe("publication UI contracts", () => {
  it("renders null as unavailable rather than zero", () => {
    render(<Metric label="Tiempo" value={null} suffix=" min" />);
    expect(screen.getByText("No disponible")).toBeInTheDocument();
    expect(screen.queryByText("0 min")).not.toBeInTheDocument();
  });

  it("renders the complete discrete legend including transfer and not evaluable", () => {
    render(<MapLegend />);
    expect(document.querySelectorAll(".legend > span")).toHaveLength(legendItems.length);
    expect(screen.getByText("Transferencia interinsular")).toBeInTheDocument();
    expect(screen.getByText("No evaluable")).toBeInTheDocument();
  });

  it("makes provenance and the clinical-time limitation visible", () => {
    render(<SourceMethodPanel />);
    expect(screen.getByText("Fuente y metodología")).toBeInTheDocument();
    expect(screen.getByText(/OSRM 5.27.1/)).toBeInTheDocument();
    expect(screen.getByText(/no representa tiempo hasta recibir atención sanitaria/i)).toBeInTheDocument();
  });

  it("renders all seven islands in the descriptive access-gap table", () => {
    render(<AccessGapTable islands={profiles.islands} />);
    for (const island of profiles.islands) expect(screen.getByRole("link", { name: island.name })).toBeInTheDocument();
    expect(screen.getByText(/sin puntuación única/i)).toBeInTheDocument();
  });

  it("renders explicit data statuses", () => {
    render(<DataBadge status="PENDING OFFICIAL GEOMETRY" />);
    expect(screen.getByText("PENDING OFFICIAL GEOMETRY")).toBeInTheDocument();
  });
});

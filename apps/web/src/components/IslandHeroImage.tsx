import Image from "next/image";
import {islandHeroByTerritory} from "@/lib/island-images";

export function IslandHeroImage({territoryId,variant="hero",priority=false}:{territoryId:string;variant?:"hero"|"card"|"credit";priority?:boolean}){
 const image=islandHeroByTerritory(territoryId);
 if(!image)return null;
 return <figure className={`island-image island-image-${variant}`} data-territory-image={territoryId}>
  <Image src={image.local_path} alt={image.alt} fill sizes={variant==="card"?"(max-width: 680px) 100vw, (max-width: 1180px) 25vw, 14vw":"(max-width: 680px) 100vw, 92vw"} priority={priority} quality={82}/>
  <figcaption className="photo-credit">Foto: <a href={image.source_url} target="_blank" rel="noreferrer">{image.author}</a> · <a href={image.license_url} target="_blank" rel="noreferrer">{image.license}</a></figcaption>
 </figure>;
}

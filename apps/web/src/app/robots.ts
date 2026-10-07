import type {MetadataRoute} from "next";
export default function robots():MetadataRoute.Robots{return {rules:{userAgent:"*",allow:"/"},sitemap:"https://pedsdata.pedscore.app/sitemap.xml",host:"https://pedsdata.pedscore.app"}}

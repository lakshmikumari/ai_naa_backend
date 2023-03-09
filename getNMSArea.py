import os
from log import logger

scriptPath = os.path.dirname(os.path.realpath(__file__))


def getNMSArea(tableName, tableToNMSMap_json):
    try:
        NMSArea = ""
        tableName = tableName.strip()
        for key in tableToNMSMap_json.keys():
            tableList = tableToNMSMap_json[key]
            if tableName in tableList:
                NMSArea = key
                break
            elif NMSArea == "":
                for item in tableList:
                    if "VSAN table" in tableName:
                        if tableName.replace("VSAN table", "Show VSAN table") in item:
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    elif "IPv4 - Router Switching Path Status (Non-Distributed Platform)" in tableName:
                        if (tableName.replace("IPv4 - Router Switching Path Status (Non-Distributed Platform)",
                                              "IPv4 - Router Switching Path Status (Non-Distributed Switching Platform)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    elif "NVE Interface Status Table" in tableName:
                        if tableName.replace("NVE Interface Status Table", "Interface nve status table") in item:
                            NMSArea = key
                            logger.info(NMSArea)
                            break

                    elif "IPv6 - Router Switching Path Status (Non-Distributed Platform)" in tableName:
                        if (tableName.replace("IPv6 - Router Switching Path Status (Non-Distributed Platform)",
                                              "IPv6 - Router Switching Path Status (Non-Distributed Switching Platform)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break

                    elif "IPv4 - Not-CEF-Switched Statistics (Non-distributed Switching Platform)" in tableName:
                        NMSArea = "Capacity Management"
                        logger.info(NMSArea)
                        break

                    elif "IPv4 - Hot Standby Routing Protocol Table" in tableName:
                        NMSArea = "Configuration Management"
                        logger.info(NMSArea)
                        break
                    elif "Summarization Related (ABRs only) - Main Domain" in tableName:
                        if (tableName.replace("Summarization Related (ABRs only) - Main Domain",
                                              "Summarization Related - Main Domain (ABRs only)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    elif "Summarization Related (ABRs only) - Other Domains" in tableName:
                        if (tableName.replace("Summarization Related (ABRs only) - Other Domains",
                                              "Summarization Related - Other Domain (ABRs only)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break

                    elif "ADMIN Distance Table (Exceptions only) - Main Domain" in tableName:
                        if (tableName.replace("ADMIN Distance Table (Exceptions only) - Main Domain",
                                              "ADMIN Distance Table - Main Domain (Exceptions only)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    elif "ADMIN Distance Table (Exceptions only) - Other Domains" in tableName:
                        if (tableName.replace("ADMIN Distance Table (Exceptions only) - Other Domains",
                                              "ADMIN Distance Table - Other Domain (Exceptions only)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break

                    elif "Catalyst 6500 Series MLS Netflow Configuration Table" in tableName:
                        if (tableName.replace("Catalyst 6500 Series MLS Netflow Configuration Table",
                                              "Catalyst 6500 and Cisco 7600 Series MLS Netflow Configuration Table") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    elif "Suspects Port Table" in tableName:
                        if tableName.replace("Suspects Port Table", "Suspect Ports Table") in item:
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    elif "SIP SPA Compatibility Table" in tableName:
                        if tableName.replace("SIP SPA Compatibility Table", "SIP and SPA Information Table") in item:
                            NMSArea = key
                            logger.info(NMSArea)
                            break


                    elif ("Cisco 6500 7600 MPLS Interface Table" in tableName):
                        if (tableName.replace("Cisco 6500 7600 MPLS Interface Table",
                                              "Cisco 6500/7600 MPLS Interface Table") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break


                    elif ("Cisco 7600 MPLS Routes VRF's HW mode Table" in tableName):
                        if (tableName.replace("Cisco 7600 MPLS Routes VRF's HW mode Table",
                                              "Cisco 7600 MPLS Routes/VRF's/HW mode Table") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break

                    elif ("Hardware Table - VSS" in tableName):
                        if (tableName.replace("Hardware Table - VSS", "Catalyst 6500 Table - VSS") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break


                    elif ("Catalyst 6500 and Cisco 7600 Series High Availability(HA)-System Audit" in tableName):
                        if (tableName.replace("Catalyst 6500 and Cisco 7600 Series High Availability(HA)-System Audit",
                                              "Catalyst 6500 and Cisco 7600 Series High Availability(HA) - System Audit") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break




                    elif ("DR BDR Implementation - Main Domain" in tableName):
                        if (tableName.replace("DR BDR Implementation - Main Domain",
                                              "DR/BDR Implementation - Main Domain") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    elif ("DR BDR Implementation - Other Domains" in tableName):
                        if (tableName.replace("DR BDR Implementation - Other Domains",
                                              "DR/BDR Implementation - Other Domain") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break



                    elif ("DR BDR Related (Exceptions only) - Main Domain" in tableName):
                        if (tableName.replace("DR BDR Related (Exceptions only) - Main Domain",
                                              "DR/BDR Related - Main Domain (Exceptions only)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    elif ("DR BDR Related (Exceptions only) - Other Domains" in tableName):
                        if (tableName.replace("DR BDR Related (Exceptions only) - Other Domains",
                                              "DR/BDR Related - Other Domain (Exceptions only)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break

                    elif ("PE-CE RIP Version 2 Authentication(IOS, IOS XR and IOS XE)" in tableName):
                        if (tableName.replace("PE-CE RIP Version 2 Authentication(IOS, IOS XR and IOS XE)",
                                              "PE-CE RIP Version 2 Authentication") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break

                    elif ("Audited ABRs in Main Domain" in tableName):
                        if (tableName.replace("Audited ABRs in Main Domain", "Audited ABRs - Main Domain") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break


                    elif ("Not Audited ABRs in Main Domain" in tableName):
                        if (tableName.replace("Not Audited ABRs in Main Domain",
                                              "Non Audited ABRs - Main Domain") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break

                    elif ("Largest Number of OSPF Routes per Type - Main Domain" in tableName):
                        NMSArea = "Configuration Management"
                        logger.info(NMSArea)
                        break
                    elif ("OSPF Memory Analysis for IOSXR" in tableName):
                        NMSArea = "Capacity Management"
                        logger.info(NMSArea)
                        break

                    elif ("OSPF SPF and LSA Throttle Timers" in tableName):
                        NMSArea = "Configuration Management"
                        logger.info(NMSArea)
                        break

                    elif ("BGP Generic Configuration Best Practices (IOS, IOS XR and IOS-XE)" in tableName):
                        if (tableName.replace("BGP Generic Configuration Best Practices (IOS, IOS XR and IOS-XE)",
                                              "BGP Generic Configuration best practices (IOS, IOS XR and IOS-XE)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break



                    elif ("OSPF Neighbor Inventory (Exceptions only) - Main Domain" in tableName):
                        if (tableName.replace("OSPF Neighbor Inventory (Exceptions only) - Main Domain",
                                              "OSPF Neighbor Inventory - Main Domain (Exceptions only)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    elif ("OSPF Neighbor Inventory (Exceptions only) - Other Domains" in tableName):
                        if (tableName.replace("OSPF Neighbor Inventory (Exceptions only) - Other Domains",
                                              "OSPF Neighbor Inventory - Other Domain (Exceptions only)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break

                    elif ("Neighbor related(Exceptions only)" in tableName):
                        if (tableName.replace("Neighbor related(Exceptions only)",
                                              "Neighbor related (Exceptions only)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break

                    elif ("IPv4 - Maximum Prefixes imported into VRF from CE EBGP peer (IOS and IOS XR)" in tableName):
                        if (tableName.replace(
                                "IPv4 - Maximum Prefixes imported into VRF from CE EBGP peer (IOS and IOS XR)",
                                "Maximum Prefixes imported into VRF from CE EBGP peer") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break

                    elif ("BGP VRF Import Best Practices" in tableName):
                        if (tableName.replace("BGP VRF Import Best Practices",
                                              "BGP VRF Import best practices") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break


                    elif ("Area 0 - Capacity - Addressing - Main Domain" in tableName):
                        if (tableName.replace("Area 0 - Capacity - Addressing - Main Domain",
                                              "Area 0 - Capacity - Addressing Table 1 - Main Domain") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    elif ("Area 0 - Capacity - Addressing - Other Domains" in tableName):
                        if (tableName.replace("Area 0 - Capacity - Addressing - Other Domains",
                                              "Area 0 - Capacity - Addressing Table 1 - Other Domain") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    elif (
                            "Redistribution - External Route - ASBR Related (Exceptions only) - Main Domain" in tableName):
                        if (tableName.replace(
                                "Redistribution - External Route - ASBR Related (Exceptions only) - Main Domain",
                                "Redistribution - External Route - ASBR Related - Main Domain (Exceptions only)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    elif (
                            "Redistribution - External Route - ASBR Related (Exceptions only) - Other Domain" in tableName):
                        if (tableName.replace(
                                "Redistribution - External Route - ASBR Related (Exceptions only) - Other Domain",
                                "Redistribution - External Route - ASBR Related - Other Domain (Exceptions only)") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    elif ("BGP Neighbor Performance and Convergence (IOS and IOS XR)" in tableName):
                        if (tableName.replace("BGP Neighbor Performance and Convergence (IOS and IOS XR)",
                                              "BGP Neighbor performance and convergence") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break

                    elif ("IPv4 - Maximum Prefixes allowed in VRF (IOS ,IOS XR and IOS-XE)" in tableName):
                        NMSArea = "Performance Management"
                        logger.info(NMSArea)
                        break

                    if ("IPv4" in tableName):
                        if (tableName.replace("IPv4", "IPV4") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    if ("Domains" in tableName):
                        if (tableName.replace("Domains", "Domain") in item):
                            NMSArea = key
                            logger.info(NMSArea)
                            break
                    if (tableName + " Table" in item):
                        NMSArea = key
                        logger.info(NMSArea)
                        break

                    if (item.lower() in tableName.lower()):
                        NMSArea = key
                        logger.info(NMSArea)
                        break

        return NMSArea
    except Exception as e:
        logger.error(e)

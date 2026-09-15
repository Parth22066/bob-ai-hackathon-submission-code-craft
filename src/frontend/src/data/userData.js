export const userProfile = {
  name: "GridGuard Customer",
  email: "user@gridguard.ai",
  serviceLocation: "Vadodara Central",
  connectionId: "GG-102938",
  serviceStatus: "Operational",
  areaRisk: "Low",
  weatherRisk: "Moderate",
  activeOutage: false,
  lastUpdated: "2:35 PM",
  phone: "+91 98765 43210",
  area: "Vadodara, Gujarat",
  serviceType: "Residential electricity connection",
};

export const customerAlerts = [
  { id: 1, category: "Weather", severity: "Warning", title: "High wind conditions expected", description: "Strong winds are expected in your area today. Power interruptions are possible.", time: "Today • 2:15 PM", unread: true, action: "View Details", path: "/user/service" },
  { id: 2, category: "Maintenance", severity: "Information", title: "Planned maintenance in your area", description: "Scheduled maintenance may temporarily affect electricity service in Vadodara Central.", time: "Today • 1:50 PM", unread: true, action: "View Outage", path: "/user/outages" },
  { id: 3, category: "Service", severity: "Success", title: "Your electricity service is operating normally", description: "No current service interruption has been detected for your connection.", time: "Today • 10:30 AM", unread: true, action: "View Service", path: "/user/service" },
  { id: 4, category: "Restoration", severity: "Success", title: "Power service restored", description: "Electricity service has been restored following scheduled maintenance.", time: "12 Sep 2026 • 4:30 PM", unread: false, action: "View Outage", path: "/user/outages" },
  { id: 5, category: "Outage", severity: "Information", title: "No active outage in your area", description: "No current service interruption is reported for Vadodara Central.", time: "11 Sep 2026 • 9:10 AM", unread: false, action: "View Outage", path: "/user/outages" },
];

export const issueTypes = [
  { id: "Power Outage", description: "Your electricity supply is completely unavailable.", icon: "outage" },
  { id: "Voltage Fluctuation", description: "Lights are flickering or voltage seems unstable.", icon: "voltage" },
  { id: "Electrical Equipment Issue", description: "Report a problem with electrical equipment connected to your service.", icon: "equipment" },
  { id: "Street / Area Electrical Issue", description: "Report a damaged pole, cable, streetlight, or electrical issue in your area.", icon: "area" },
  { id: "Other", description: "Report another electricity-related issue.", icon: "other" },
];

export const reportHistory = [
  { id: "GG-10391", type: "Voltage Fluctuation", date: "Sep 10", status: "Resolved", location: "Vadodara Central" },
  { id: "GG-10277", type: "Street / Area Electrical Issue", date: "Sep 04", status: "Resolved", location: "Vadodara Central" },
];

export const serviceEvents = [
  ["15 Sep 2026", "Service operating normally", "Available"],
  ["12 Sep 2026", "Power interruption", "Resolved • 42 minutes"],
  ["08 Sep 2026", "Scheduled maintenance", "Completed"],
];

export const recentServiceActivity = [
  ["Today", "Service operating normally"],
  ["Yesterday", "Weather advisory issued"],
  ["12 Sep 2026", "Scheduled maintenance completed"],
  ["08 Sep 2026", "Service interruption resolved"],
];

// import React, { useState } from "react";

// export default function Dashboard() {
//   const [searchQuery, setSearchQuery] = useState("");
//   const [selectedPerson, setSelectedPerson] = useState(null);
//   const [mode, setMode] = useState(null);
//   const [data, setData] = useState([]);
//   const [isLoading, setIsLoading] = useState(false);
//   const [generatedContent, setGeneratedContent] = useState("");

//   const runSearch = async () => {
//     if (!searchQuery) return;

//     setIsLoading(true);
//     setSelectedPerson(null);
//     setData([]);

//     try {
//       const res = await fetch("http://localhost:5001/api/search_events", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ query: searchQuery })
//       });

//       const json = await res.json();

//       if (res.ok) {
//         setData(json);
//       } else {
//         alert("Backend error: " + json.error);
//       }
//     } catch (err) {
//       console.error("Fetch error:", err);
//       alert("Failed to connect to backend.");
//     }

//     setIsLoading(false);
//   };

//   const generateAIContent = async (person, type) => {
//     setGeneratedContent("Loading...");
//     setSelectedPerson(person);
//     setMode(type);

//     const prompt = type === "rationale"
//       ? `You are a B2B sales researcher. Based on the following contact info, write a concise one sentence for each 'Why It’s a Qualified Lead:' using categories like Industry Fit, Size & Revenue, Strategic Relevance, Industry Engagement, Market Activity, and Decision-Maker Identified.\n\nData:\nCompany: ${person.Company}\nIndustry: ${person.Industry}\nRevenue: ${person.Revenue}\nSize: ${person.Size}\nEvent: ${person.Event}\nTitle: ${person.Title}\nName: ${person.Name} Should be similar to this:
//       Industry Fit: Specializes in large-format signage, vehicle wraps, and architectural graphics.
//       Size & Revenue: A global company with $8B+ in revenue and thousands of employees.
//       Strategic Relevance: A major player in the signage and graphics industry, with potential overlap in applications for Tedlar’s protective films.
//       Industry Engagement: Exhibits at key trade shows like ISA Sign Expo and is active in relevant industry associations.
//       Market Activity: Expands into durable, weather-resistant graphic films, aligning with Tedlar’s value proposition.
//       Decision-Maker Identified: Likely stakeholders include VPs of Product Development, Directors of Innovation, and R&D leaders focused on coatings and protective solutions.`
//       : `You are a B2B sales assistant. Craft a personalized outreach message for a lead based on the following data:\n\nName: ${person.Name}\nCompany: ${person.Company}\nEvent: ${person.Event}\nTitle: ${person.Title}\nIndustry: ${person.Industry}\nRevenue: ${person.Revenue}\nSize: ${person.Size}\n\nKeep it short and sweet but seem eager to learn more about the company while also pitching how you could help with minimal context. Like a LinkedIn connection note, under 300 characters.`;

//     try {
//       const res = await fetch("http://localhost:5001/api/generate_content", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ prompt })
//       });

//       const json = await res.json();
//       setGeneratedContent(json.content || "Failed to generate content.");
//     } catch (err) {
//       setGeneratedContent("Failed to fetch AI response.");
//     }
//   };

//   return (
//     <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif", background: "#f9fafb", minHeight: "100vh" }}>
//       <h1 style={{ fontSize: "2.25rem", fontWeight: "bold", color: "#111827", marginBottom: "1.5rem" }}>
//         Lead Generation Dashboard
//       </h1>

//       <form
//         onSubmit={(e) => {
//           e.preventDefault();
//           runSearch();
//         }}
//         style={{ marginBottom: "2rem" }}
//       >
//         <input
//           type="text"
//           value={searchQuery}
//           placeholder="Search trade shows or relevant industry events..."
//           onChange={(e) => setSearchQuery(e.target.value)}
//           style={{
//             padding: "0.75rem",
//             width: "100%",
//             maxWidth: "500px",
//             border: "1px solid #ccc",
//             borderRadius: "6px",
//             marginRight: "0.5rem",
//           }}
//         />
//         <button
//           type="submit"
//           style={{
//             padding: "0.75rem 1rem",
//             background: "#2563eb",
//             color: "white",
//             border: "none",
//             borderRadius: "6px",
//             cursor: "pointer"
//           }}
//         >
//           Search
//         </button>
//       </form>

//       {isLoading && <p style={{ marginBottom: "1rem" }}>🔄 Generating lead list… Please wait.</p>}

//       <div style={{
//         display: "grid",
//         gridTemplateColumns: "1fr",
//         gap: "1.5rem",
//         maxWidth: "100%",
//       }}>
//         {data.map((row, idx) => (
//           <div key={idx} style={{
//             background: "white",
//             padding: "1.5rem",
//             borderRadius: "12px",
//             boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
//             transition: "0.2s",
//             border: "1px solid #e5e7eb"
//           }}>
//             <div style={{
//               display: "grid",
//               gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
//               gap: "0.5rem 2rem"
//             }}>
//               <p><strong>Company:</strong> {row.Company}</p>
//               <p><strong>Name:</strong> {row.Name}</p>
//               <p><strong>Title:</strong> {row.Title}</p>
//               <p><strong>Email:</strong> {row.Email}</p>
//               <p><strong>Phone:</strong> {row.Phone}</p>
//               <p><strong>LinkedIn:</strong> <a href={row.LinkedIn} target="_blank" rel="noreferrer">Profile</a></p>
//               <p><strong>Location:</strong> {row.Location}</p>
//               <p><strong>Revenue:</strong> {row.Revenue}</p>
//               <p><strong>Size:</strong> {row.Size} people</p>
//             </div>

//             <div style={{ display: "flex", gap: "1rem", marginTop: "1.25rem" }}>
//               <button
//                 style={{ padding: "0.5rem 1rem", background: "#e5e7eb", border: "none", borderRadius: "6px", cursor: "pointer" }}
//                 onClick={() => generateAIContent(row, "rationale")}
//               >
//                 Rationale
//               </button>
//               <button
//                 style={{ padding: "0.5rem 1rem", background: "#2563eb", color: "white", border: "none", borderRadius: "6px", cursor: "pointer" }}
//                 onClick={() => generateAIContent(row, "outreach")}
//               >
//                 Outreach
//               </button>
//             </div>
//           </div>
//         ))}
//       </div>

//       {selectedPerson && (
//         <div style={{
//           position: "fixed", top: 0, left: 0,
//           width: "100vw", height: "100vh",
//           background: "rgba(0,0,0,0.5)",
//           display: "flex", justifyContent: "center", alignItems: "center"
//         }}>
//           <div style={{
//             background: "white", padding: "2rem", borderRadius: "10px",
//             maxWidth: "700px", width: "90%", maxHeight: "80vh", overflowY: "auto"
//           }}>
//             <h3 style={{ fontSize: "1.5rem", fontWeight: "bold", marginBottom: "1rem" }}>
//               {mode === "rationale" ? "Why It's a Qualified Lead:" : "Personalized Outreach Message"}
//             </h3>
//             <pre style={{ whiteSpace: "pre-wrap" }}>{generatedContent}</pre>
//             <button
//               style={{ marginTop: "1rem", padding: "0.5rem 1rem", background: "#dc2626", color: "white", border: "none", borderRadius: "6px" }}
//               onClick={() => setSelectedPerson(null)}
//             >
//               Close
//             </button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

import React, { useState } from "react";

export default function Dashboard() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedPerson, setSelectedPerson] = useState(null);
  const [mode, setMode] = useState(null);
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [generatedContent, setGeneratedContent] = useState("");

  const runSearch = async () => {
    if (!searchQuery) return;

    setIsLoading(true);
    setSelectedPerson(null);
    setData([]);

    try {
      const res = await fetch("http://localhost:5001/api/search_events", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: searchQuery }),
      });

      const json = await res.json();

      if (res.ok) {
        setData(json);
      } else {
        alert("Backend error: " + json.error);
      }
    } catch (err) {
      console.error("Fetch error:", err);
      alert("Failed to connect to backend.");
    }

    setIsLoading(false);
  };

  const generateAIContent = async (person, type) => {
    setGeneratedContent("Loading...");
    setSelectedPerson(person);
    setMode(type);

    const prompt = type === "rationale"
          ? `You are a B2B sales researcher. Based on the following contact info, write a concise one sentence for each 'Why It’s a Qualified Lead:' using categories like Industry Fit, Size & Revenue, Strategic Relevance, Industry Engagement, Market Activity, and Decision-Maker Identified.\n\nData:\nCompany: ${person.Company}\nIndustry: ${person.Industry}\nRevenue: ${person.Revenue}\nSize: ${person.Size}\nEvent: ${person.Event}\nTitle: ${person.Title}\nName: ${person.Name} Should be similar to this:
          Industry Fit: Specializes in large-format signage, vehicle wraps, and architectural graphics.
          Size & Revenue: A global company with $8B+ in revenue and thousands of employees.
          Strategic Relevance: A major player in the signage and graphics industry, with potential overlap in applications for Tedlar’s protective films.
          Industry Engagement: Exhibits at key trade shows like ISA Sign Expo and is active in relevant industry associations.
          Market Activity: Expands into durable, weather-resistant graphic films, aligning with Tedlar’s value proposition.
          Decision-Maker Identified: Likely stakeholders include VPs of Product Development, Directors of Innovation, and R&D leaders focused on coatings and protective solutions.`
          : `You are a B2B sales assistant. Craft a personalized outreach message for a lead based on the following data:\n\nName: ${person.Name}\nCompany: ${person.Company}\nEvent: ${person.Event}\nTitle: ${person.Title}\nIndustry: ${person.Industry}\nRevenue: ${person.Revenue}\nSize: ${person.Size}\n\nKeep it short and sweet but seem eager to learn more about the company while also pitching how you could help with minimal context. Like a LinkedIn connection note, under 300 characters.`;

    
    try {
      const res = await fetch("http://localhost:5001/api/generate_content", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      const json = await res.json();
      setGeneratedContent(json.content || "Failed to generate content.");
    } catch (err) {
      setGeneratedContent("Failed to fetch AI response.");
    }
  };

  return (
    <div
      style={{
        padding: "2rem",
        fontFamily: "Arial, sans-serif",
        background: "#f9fafb",
        minHeight: "100vh",
      }}
    >
      <h1
        style={{
          fontSize: "2.25rem",
          fontWeight: "bold",
          color: "#111827",
          marginBottom: "1.5rem",
        }}
      >
        Lead Generation Dashboard
      </h1>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          runSearch();
        }}
        style={{ marginBottom: "2rem" }}
      >
        <input
          type="text"
          value={searchQuery}
          placeholder="Search trade shows or relevant industry events..."
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{
            padding: "0.75rem",
            width: "100%",
            maxWidth: "500px",
            border: "1px solid #ccc",
            borderRadius: "6px",
            marginRight: "0.5rem",
          }}
        />
        <button
          type="submit"
          style={{
            padding: "0.75rem 1rem",
            background: "#2563eb",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
          }}
        >
          Search
        </button>
      </form>

      {isLoading && (
        <p style={{ marginBottom: "1rem" }}>
          🔄 Generating lead list… Please wait.
        </p>
      )}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr",
          gap: "1.5rem",
          maxWidth: "100%",
        }}
      >
        {data.map((row, idx) => (
          <div
            key={idx}
            style={{
              background: "white",
              padding: "1.5rem",
              borderRadius: "12px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
              transition: "0.2s",
              border: "1px solid #e5e7eb",
            }}
          >
            <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              <p style={{ wordWrap: "break-word", whiteSpace: "normal" }}>
                <strong>Event:</strong> {row.Event}
              </p>
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
                  gap: "0.5rem 2rem",
                }}
              >
                <p><strong>Company:</strong> {row.Company}</p>
                <p><strong>Name:</strong> {row.Name}</p>
                <p><strong>Title:</strong> {row.Title}</p>
                <p><strong>Email:</strong> {row.Email}</p>
                <p><strong>Phone:</strong> {row.Phone}</p>
                <p>
                  <strong>LinkedIn:</strong>{" "}
                  <a href={row.LinkedIn} target="_blank" rel="noreferrer">
                    Profile
                  </a>
                </p>
                <p><strong>Location:</strong> {row.Location}</p>
                <p><strong>Revenue:</strong> {row.Revenue}</p>
                <p><strong>Size:</strong> {row.Size} people</p>
                <p><strong>Industry:</strong> {row.Industry}</p>
              </div>
            </div>

            <div
              style={{ display: "flex", gap: "1rem", marginTop: "1.25rem" }}
            >
              <button
                style={{
                  padding: "0.5rem 1rem",
                  background: "#e5e7eb",
                  border: "none",
                  borderRadius: "6px",
                  cursor: "pointer",
                }}
                onClick={() => generateAIContent(row, "rationale")}
              >
                Rationale
              </button>
              <button
                style={{
                  padding: "0.5rem 1rem",
                  background: "#2563eb",
                  color: "white",
                  border: "none",
                  borderRadius: "6px",
                  cursor: "pointer",
                }}
                onClick={() => generateAIContent(row, "outreach")}
              >
                Outreach
              </button>
            </div>
          </div>
        ))}
      </div>

      {selectedPerson && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            background: "rgba(0,0,0,0.5)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div
            style={{
              background: "white",
              padding: "2rem",
              borderRadius: "10px",
              maxWidth: "700px",
              width: "90%",
              maxHeight: "80vh",
              overflowY: "auto",
            }}
          >
            <h3
              style={{
                fontSize: "1.5rem",
                fontWeight: "bold",
                marginBottom: "1rem",
              }}
            >
              {mode === "rationale"
                ? "Why It's a Qualified Lead:"
                : "Personalized Outreach Message"}
            </h3>
            <pre style={{ whiteSpace: "pre-wrap" }}>{generatedContent}</pre>
            <button
              style={{
                marginTop: "1rem",
                padding: "0.5rem 1rem",
                background: "#dc2626",
                color: "white",
                border: "none",
                borderRadius: "6px",
              }}
              onClick={() => setSelectedPerson(null)}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
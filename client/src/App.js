import React, { useEffect, useState } from "react";

const App = () => {
  const [songs, setSongs] = useState([]);
  const [selectedSongs, setSelectedSongs] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [recommendedSongs, setRecommendedSongs] = useState([]);
  const [modelVersion, setModelVersion] = useState("");
  const [modelDate, setModelDate] = useState("");
  const [isModalVisible, setIsModalVisible] = useState(false);

  useEffect(() => {
    const songs_path = process.env.REACT_APP_SONGS_PATH;
    fetch(songs_path)
      .then((response) => {
        if (response.ok) return response.text();
        throw new Error("Failed to fetch the CSV file");
      })
      .then((csvText) => {
        const parsedData = csvText
          .split("\n")
          .slice(1) // skip header
          .map((line) => {
            const [artist_name, track_name] = line.split(",");
            return {
              artist_name: artist_name.trim(),
              track_name: track_name.trim(),
            };
          });
        setSongs(parsedData);
      })
      .catch((error) => alert("Error loading CSV: " + error.message));
  }, []);

  const addSongToList = (record) => {
    if (
      !selectedSongs.find(
        (song) =>
          song.artist_name === record.artist_name &&
          song.track_name === record.track_name
      )
    ) {
      setSelectedSongs((prev) => [...prev, record]);
      alert(
        `Added "${record.track_name}" by ${record.artist_name} to the list!`
      );
    } else {
      alert(
        `"${record.track_name}" by ${record.artist_name} is already in the list.`
      );
    }
  };

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const filteredSongs = songs.filter((song) => {
    return (
      song.artist_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      song.track_name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  });

  const handleGenerateRecommendation = async () => {
    const track_names = selectedSongs.map((song) => song.track_name);
    const body = { songs: track_names };

    try {
      const response = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (response.ok) {
        const data = await response.json();
        setRecommendedSongs(data.songs || []);
        setModelVersion(data.version);
        setModelDate(data.model_date);
        setIsModalVisible(true);
      } else {
        alert("Failed to generate recommendation.");
      }
    } catch (error) {
      alert("Error connecting to the server.");
    }
  };

  const handleCloseModal = () => {
    setIsModalVisible(false);
    setRecommendedSongs([]);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Song Selector</h1>

      {selectedSongs.length > 0 && (
        <div style={{ marginBottom: "20px" }}>
          <h2>Selected Songs</h2>
          <ul>
            {selectedSongs.map((item, index) => (
              <li key={index}>
                {item.artist_name} - {item.track_name}
              </li>
            ))}
          </ul>
          <button onClick={handleGenerateRecommendation}>
            Generate Recommendation
          </button>
        </div>
      )}

      <input
        type="text"
        placeholder="Search for songs..."
        value={searchTerm}
        onChange={handleSearchChange}
        style={{ width: 300, marginBottom: "20px" }}
      />

      {filteredSongs.length > 0 ? (
        <>
          <h2>Available Songs</h2>
          <table>
            <thead>
              <tr>
                <th>Artist</th>
                <th>Track</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredSongs.map((song, index) => (
                <tr key={index}>
                  <td>{song.artist_name}</td>
                  <td>{song.track_name}</td>
                  <td>
                    <button onClick={() => addSongToList(song)}>Add</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      ) : (
        <p>No songs found matching the search criteria.</p>
      )}

      {isModalVisible && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: "rgba(0,0,0,0.5)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div
            style={{
              background: "white",
              padding: "20px",
              borderRadius: "8px",
              width: "300px",
            }}
          >
            <h2>Recommended Songs</h2>
            <p>
              <strong>Version:</strong> {modelVersion}
            </p>
            <p>
              <strong>Model Date:</strong> {modelDate}
            </p>
            <ul>
              {recommendedSongs.map((song, index) => (
                <li key={index}>{song}</li>
              ))}
            </ul>
            <button onClick={handleCloseModal}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;

import React, { useEffect, useState } from "react";
import { Table, Button, List, message, Input, Modal } from "antd";
import Papa from "papaparse";
import axios from "axios";

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
        const parsedData = Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          dynamicTyping: true,
          delimiter: ",",
        });

        const formattedData = parsedData.data.map((song) => ({
          ...song,
          artist_name: String(song.artist_name),
          track_name: String(song.track_name),
        }));

        setSongs(formattedData);
      })
      .catch((error) => {
        message.error("Error loading CSV: " + error.message);
      });
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
      message.success(
        `Added "${record.track_name}" by ${record.artist_name} to the list!`
      );
    } else {
      message.warning(
        `"${record.track_name}" by ${record.artist_name} is already in the list.`
      );
    }
  };

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const filteredSongs = songs.filter((song) => {
    return (
      song.artist_name.includes(searchTerm) ||
      song.track_name.includes(searchTerm)
    );
  });

  const columns = [
    { title: "Artist", dataIndex: "artist_name", key: "artist" },
    { title: "Track", dataIndex: "track_name", key: "track" },
    {
      title: "Action",
      key: "action",
      render: (_, record) => (
        <Button type="primary" onClick={() => addSongToList(record)}>
          Add
        </Button>
      ),
    },
  ];

  const handleGenerateRecommendation = async () => {
    const track_names = selectedSongs.map((song) => song.track_name);

    const body = {
      songs: track_names,
    };

    try {
      const response = await axios.post("/api/recommend", body);

      if (response.status === 200) {
        const data = response.data;
        console.log(data);
        setRecommendedSongs(data.songs || []);
        setModelVersion(data.version);
        setModelDate(data.model_date);
        setIsModalVisible(true);
      } else {
        message.error("Failed to generate recommendation.");
      }
    } catch (error) {
      message.error("Error connecting to the server.");
      console.error(error);
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
          <List
            bordered
            dataSource={selectedSongs}
            style={{ marginBottom: "10px" }}
            renderItem={(item) => (
              <List.Item>
                {item.artist_name} - {item.track_name}
              </List.Item>
            )}
          />
          <Button type="primary" onClick={handleGenerateRecommendation}>
            Generate Recommendation
          </Button>
        </div>
      )}

      <Input
        placeholder="Search for songs..."
        value={searchTerm}
        onChange={handleSearchChange}
        style={{ width: 300, marginBottom: "20px" }}
      />

      {filteredSongs.length > 0 ? (
        <>
          <h2>Available Songs</h2>
          <Table
            dataSource={filteredSongs}
            columns={columns}
            rowKey="track_name"
          />
        </>
      ) : (
        <p>No songs found matching the search criteria.</p>
      )}

      <Modal
        title="Recommended Songs"
        open={isModalVisible}
        onCancel={handleCloseModal}
        footer={[
          <Button key="close" onClick={handleCloseModal}>
            Close
          </Button>,
        ]}
      >
        <p>
          <strong>Version:</strong> {modelVersion}
        </p>
        <p>
          <strong>Model Date:</strong> {modelDate}
        </p>
        <List
          bordered
          dataSource={recommendedSongs}
          renderItem={(song, index) => (
            <List.Item key={index}>{song}</List.Item>
          )}
        />
      </Modal>
    </div>
  );
};

export default App;

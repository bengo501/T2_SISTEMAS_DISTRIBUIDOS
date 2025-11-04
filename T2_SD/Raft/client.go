package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"sync"
	"time"
)

type Client struct {
	id          int
	raftURLs    []string
	duration    time.Duration
	latencies   []float64
	requests    int
	mu          sync.Mutex
	startTime   time.Time
	requestData []byte
}

func NewClient(id int, raftURLs []string, duration time.Duration) *Client {
	return &Client{
		id:          id,
		raftURLs:    raftURLs,
		duration:    duration,
		latencies:   make([]float64, 0),
		requestData: []byte(fmt.Sprintf("request-%d", id)),
	}
}

func (c *Client) Run() {
	c.startTime = time.Now()

	for time.Since(c.startTime) < c.duration {
		leaderURL := c.pickLeader()
		if leaderURL == "" {
			time.Sleep(100 * time.Millisecond)
			continue
		}

		t1 := time.Now()
		if c.sendRequest(leaderURL) {
			lat := time.Since(t1).Seconds()
			c.mu.Lock()
			c.latencies = append(c.latencies, lat)
			c.requests++
			c.mu.Unlock()
		}

		time.Sleep(10 * time.Millisecond)
	}
}

func (c *Client) pickLeader() string {
	for _, url := range c.raftURLs {
		if c.isLeader(url) {
			return url
		}
	}
	return ""
}

func (c *Client) isLeader(url string) bool {
	resp, err := http.Get(url + "/status")
	if err != nil {
		return false
	}
	defer resp.Body.Close()

	var status struct {
		State string `json:"state"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&status); err != nil {
		return false
	}
	return status.State == "StateLeader"
}

func (c *Client) sendRequest(url string) bool {
	req := map[string]string{"data": string(c.requestData)}
	data, err := json.Marshal(req)
	if err != nil {
		return false
	}

	resp, err := http.Post(url+"/propose", "application/json", bytes.NewReader(data))
	if err != nil {
		return false
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	var result map[string]interface{}
	if err := json.Unmarshal(body, &result); err != nil {
		return false
	}

	return resp.StatusCode == http.StatusOK && result["success"] == true
}

func (c *Client) GetMetrics() (throughput float64, avgLatency float64, latencies []float64) {
	c.mu.Lock()
	defer c.mu.Unlock()

	totalTime := time.Since(c.startTime).Seconds()
	if totalTime == 0 {
		return 0, 0, c.latencies
	}

	throughput = float64(c.requests) / totalTime

	sum := 0.0
	for _, lat := range c.latencies {
		sum += lat
	}
	if len(c.latencies) > 0 {
		avgLatency = sum / float64(len(c.latencies))
	}

	return throughput, avgLatency, c.latencies
}

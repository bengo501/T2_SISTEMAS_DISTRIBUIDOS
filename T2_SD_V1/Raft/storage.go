package main

import (
	"sync"

	"go.etcd.io/raft/v3"
	"go.etcd.io/raft/v3/raftpb"
)

type memoryStorage struct {
	sync.Mutex
	raft.MemoryStorage
}

func newMemoryStorage() *memoryStorage {
	return &memoryStorage{
		MemoryStorage: *raft.NewMemoryStorage(),
	}
}

func (m *memoryStorage) InitialState() (raftpb.HardState, raftpb.ConfState, error) {
	m.Lock()
	defer m.Unlock()
	return m.MemoryStorage.InitialState()
}

func (m *memoryStorage) SetHardState(st raftpb.HardState) error {
	m.Lock()
	defer m.Unlock()
	return m.MemoryStorage.SetHardState(st)
}

func (m *memoryStorage) Append(entries []raftpb.Entry) error {
	m.Lock()
	defer m.Unlock()
	return m.MemoryStorage.Append(entries)
}

func (m *memoryStorage) ApplySnapshot(snap raftpb.Snapshot) error {
	m.Lock()
	defer m.Unlock()
	return m.MemoryStorage.ApplySnapshot(snap)
}

func (m *memoryStorage) Entries(lo, hi, maxSize uint64) ([]raftpb.Entry, error) {
	m.Lock()
	defer m.Unlock()
	return m.MemoryStorage.Entries(lo, hi, maxSize)
}

func (m *memoryStorage) Term(i uint64) (uint64, error) {
	m.Lock()
	defer m.Unlock()
	return m.MemoryStorage.Term(i)
}

func (m *memoryStorage) LastIndex() (uint64, error) {
	m.Lock()
	defer m.Unlock()
	return m.MemoryStorage.LastIndex()
}

func (m *memoryStorage) FirstIndex() (uint64, error) {
	m.Lock()
	defer m.Unlock()
	return m.MemoryStorage.FirstIndex()
}

func (m *memoryStorage) Snapshot() (raftpb.Snapshot, error) {
	m.Lock()
	defer m.Unlock()
	return m.MemoryStorage.Snapshot()
}

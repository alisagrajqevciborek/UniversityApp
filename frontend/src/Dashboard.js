import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('access');
    if (!token) {
      window.location.href = '/login';
      return;
    }
    axios
      .get('http://127.0.0.1:8000/api/dashboard/', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setData(res.data))
      .catch(err => setError('Could not fetch dashboard data'));
  }, []);

  if (error) return <div>{error}</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      <h2>Dashboard ({data.role})</h2>
      {data.role === 'administrator' && (
        <div>
          <p>Professors: {data.professors}</p>
          <p>Students: {data.students}</p>
          <p>Subjects: {data.subjects}</p>
        </div>
      )}
      {data.role === 'professor' && (
        <div>
          <h3>Your subjects</h3>
          <ul>{data.subjects.map(s => <li key={s.id}>{s.code} - {s.title}</li>)}</ul>
        </div>
      )}
      {data.role === 'student' && (
        <div>
          <h3>Your subjects</h3>
          <ul>{data.subjects.map(s => <li key={s.id}>{s.code} - {s.title}</li>)}</ul>
        </div>
      )}
    </div>
  );
}

'use client'
import { useState } from 'react'
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts'
import styles from './page.css'

export default function Home() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(false)

  const handleScrape = async () => {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/scrape', { method: 'POST' })
      const json = await res.json()
      setData(json)
      console.log('Received data:', json)
    } catch (err) {
      console.error('Error fetching data:', err)
    } finally {
      setLoading(false)
    }
  }

  const sentimentCount = data.reduce((acc, item) => {
    acc[item.sentiment] = (acc[item.sentiment] || 0) + 1
    return acc
  }, {})

  const sentimentData = Object.keys(sentimentCount).map((key) => ({
    name: key,
    value: sentimentCount[key],
  }))

  const COLORS = ['#00C49F', '#FF8042', '#8884d8'] // Customize colors

  return (
    <main className="page">
      <h1>Daraz Review Dashboard</h1>
      <button onClick={handleScrape}>
        {loading ? 'Scraping...' : 'Start Scraping'}
      </button>

      {data.length > 0 && (
        <>
          <div className="chartContainer">
            <PieChart width={400} height={300}>
              <Pie
                data={sentimentData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                dataKey="value"
              >
                {sentimentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </div>

          <div className={styles.tableContainer}>
            <table>
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Review</th>
                  <th>Rating</th>
                  <th>Sentiment</th>
                </tr>
              </thead>
              <tbody>
                {data.map((row, i) => (
                  <tr key={i}>
                    <td>{row.product}</td>
                    <td>{row.review}</td>
                    <td>{row.rating}</td>
                    <td>{row.sentiment}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </main>
  )
}

import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
      <h1>Welcome to Sorting Hat</h1>
      <Link to="/upload">
        <button>Upload CSV to Start</button>
      </Link>
    </div>
  );
};

export default Home;

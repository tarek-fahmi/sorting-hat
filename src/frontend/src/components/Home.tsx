import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
      <h1>Welcome to Sorting Hat Application</h1>
      <Link to="/upload">
        <button>Press to Start</button>
      </Link>
    </div>
  );
};

export default Home;

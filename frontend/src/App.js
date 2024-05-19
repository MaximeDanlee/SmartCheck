import './App.css';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';

// Importing components
import NavbarMenu from './components/Navbar/NavbarMenu';
import Home from './components/Home/Home';
// import Settings from './components/Settings/Settings';

function App() {
  return (
     <Router>
      <div className="App" style={{margin: 0, padding: 0 }}>
        <NavbarMenu />
        <Routes>
            <Route path="/" exact element={<Home />} />
            {/* <Route path={"/settings"} element={<Settings />} /> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;

import { useNavigate } from "react-router-dom";

const HomePage = (props) => {
  const navigate = useNavigate();

  return (
    <div className="et-homePage">
      <div className="et-homePage__header">
        <span className="pt-3 pt-md-20 pt-lg-13">Prevent to getting
          <br /> {/*line break */}
          scammed</span>
      </div>
      <div className="et-homePage__content p-20 px-md-10 px-lg-21">
        <div className="et-homePage__content__text">
          {props.mode === "test" &&
            < h1 > Welcome to the Test</h1>
          }
          {props.mode === "educational" &&
            <h1>Welcome to the Educational Test</h1>
          }
          <h5 className="pt-3">This is a study to teach you how could you getting scammed.</h5>
          <p className="py-20">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna al  iqua. Ut enim ad minim veniam.</p>
        </div>
        <button className="et-homePage__content__button" onClick={() => navigate("/workflow/" + props.id)}>Get Started</button>
      </div>
    </div >
  );
}

export default HomePage;

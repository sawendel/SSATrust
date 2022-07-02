import { useNavigate } from "react-router-dom";
import { useQuery } from '../../hooks';

const HomePage = (props) => {
  const navigate = useNavigate();
  const query = useQuery();

  return (
    <div className="et-homePage">
      <div className="et-homePage__header">
        <span className="pt-3 pt-md-20 pt-lg-13">Research on
          <br /> {/*line break */}
          imposter scams</span>
      </div>
      <div className="et-homePage__content p-20 px-md-10 px-lg-21">
        <div className="et-homePage__content__text">
          {props.mode === "test" &&
            < h1 > Welcome to the Test Sequence, for the Social Security Trust Project.</h1>
          }
          {props.mode === "educational" &&
            <h1>Welcome to the Training Sequence, for the Social Security Trust Project.</h1>
          }
          <h5 className="pt-3">This site hosts a research study from the University of Wisconsin.</h5>
          <p className="py-20">The Social Security Administration provided a series of grants to the University of Wisconsin, Center for Financial Security, 
		  to better understand the effects of impostors scams: when scammers trick people into providing personal information online by posing as the SSA or other organizations. 
		  The current study, conducted by researchers Cliff Robb, Steve Wendel and Marti DeLiema, investigates how to help people recognize legiimate communications versus scams. 
		  More information about the current study can be found on the University of Wisconsin Website, at <a href="https://cfsrdrc.wisc.edu/project/wi22-10">https://cfsrdrc.wisc.edu/project/wi22-10</a></p>
        </div>
		<!--
        <button className="et-homePage__content__button" onClick={() => navigate(`/workflow/${props.id}?${query.toString()}`)}>Get Started</button>
		-->
      </div>
    </div >
  );
}

export default HomePage;

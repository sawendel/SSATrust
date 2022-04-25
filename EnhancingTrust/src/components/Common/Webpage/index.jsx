import { useState } from 'react';
import { Row, Col, Image } from 'react-bootstrap';
import TemplateRenderer from '../TemplateRenderer';

const Webpage = (props) => {
  const [config, setConfig] = useState();

  return (
    <div className="et-webpage px-lg-4 py-lg-3">
      <div className="et-webpage__window">
        <div className="et-webpage__tabbar px-3 pt-2 d-none d-lg-flex">
          <div className="et-webpage__tabbar-btn-close" />
          <div className="et-webpage__tabbar-btn-minimize" />
          <div className="et-webpage__tabbar-btn-maximize" />
          <div className="et-webpage__tabbar-tab p-2">
            <img alt="Tab favicon" src={config?.tabIcon} width="16" height="16" />
            <small className="text-truncate" title={config?.tabName}>{config?.tabName}</small>
            <small><i className="et-close" /></small>
          </div>
          <small><i className="et-plus" /></small>
        </div>
        <div className="et-webpage__toolbar px-3 py-1">
          <Row className="align-items-center">
            <Col xs="auto" className="d-none d-lg-block">
              <div className="et-webpage__toolbar-actions">
                <small><i className="et-prev" /></small>
                <small><i className="et-next text-sylver" /></small>
                <small><i className="et-refresh" /></small>
                <small><i className="et-home" /></small>
              </div>
            </Col>
            <Col>
              <div className="et-webpage__toolbar-nav px-3 py-2">
                <small className="me-3"><i className="et-lock-fill" /></small>
                <small>{config?.url}</small>
                <small className="ms-auto d-none d-lg-block"><i className="et-star" /></small>
              </div>
            </Col>
            <Col xs="auto" className="d-none d-lg-block">
              <div className="d-flex align-items-center">
                <div className="me-3">
                  <Image
                    alt="profile"
                    src="https://ui-avatars.com/api/?name=R&background=11B1C1&color=fff&rounded=true&size=22"
                    roundedCircle
                  />
                </div>
                <small className="mt-1"><i className="et-dots" /></small>
              </div>
            </Col>
          </Row>
        </div>
        <TemplateRenderer {...props} setOptions={setConfig} />
      </div>
    </div>
  )
};

export default Webpage;
import { useState } from 'react';
import { Button, Row, Col, Image } from 'react-bootstrap';
import TemplateRenderer from '../TemplateRenderer';
import Tooltip from '../Tooltip';
import { events } from '../../../constants';

const Webpage = ({ showTooltips, ...props }) => {
  const [config, setConfig] = useState();

  return (
    <div className="et-webpage px-lg-4 py-lg-3">
      <div className="et-webpage__window">
        <div className="et-webpage__tabbar px-3 pt-2 d-none d-lg-flex">
          <div className="et-webpage__tabbar-btn-close" />
          <div className="et-webpage__tabbar-btn-minimize" />
          <div className="et-webpage__tabbar-btn-maximize" />
          <div className="et-webpage__tabbar-tab p-2">
            {config?.tabIcon && <img alt="Tab favicon" src={config?.tabIcon} width="16" height="16" />}
            <small className="text-truncate" title={config?.tabName}>{config?.tabName}</small>
            <Button variant="link" className="et-event__btn" onClick={() => props.logEvent(events.BROWSER_CLOSE_TAB_CLICKED)}>
              <small><i className="et-close" /></small>
            </Button>
          </div>
          <Button variant="link" className="et-event__btn" onClick={() => props.logEvent(events.BROWSER_NEW_TAB_CLICKED)}>
            <small><i className="et-plus" /></small>
          </Button>
        </div>
        <div className="et-webpage__toolbar px-3 py-1">
          <Row className="align-items-center">
            <Col xs="auto" className="d-none d-lg-block">
              <div className="et-webpage__toolbar-actions">
                <Button variant="link" className="et-event__btn" onClick={() => props.logEvent(events.BROWSER_BACK_CLICKED)}>
                  <small><i className="et-prev" /></small>
                </Button>
                <Button variant="link" className="et-event__btn" onClick={() => props.logEvent(events.BROWSER_NEXT_CLICKED)}>
                  <small><i className="et-next text-sylver" /></small>
                </Button>
                <Button variant="link" className="et-event__btn" onClick={() => props.logEvent(events.BROWSER_REFRESH_CLICKED)}>
                  <small><i className="et-refresh" /></small>
                </Button>
                <Button variant="link" className="et-event__btn" onClick={() => props.logEvent(events.BROWSER_HOME_CLICKED)}>
                  <small><i className="et-home" /></small>
                </Button>
              </div>
            </Col>
            <Col className="text-truncate">
              <div className="et-webpage__toolbar-nav px-3 py-2">
                <small className="me-3"><i className="et-lock-fill" /></small>
                <Tooltip show={showTooltips} text={config?.urlTooltip} placement="bottom">
                  <small className="text-truncate">{config?.url}</small>
                </Tooltip>
                <Button variant="link" className="et-event__btn ms-auto d-none d-lg-block" onClick={() => props.logEvent(events.BROWSER_MARK_FAVORITE_CLICKED)}>
                  <small><i className="et-star" /></small>
                </Button>
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
                <Button variant="link" className="mt-1 et-event__btn" onClick={() => props.logEvent(events.BROWSER_DOTS_CLICKED)}>
                  <small><i className="et-dots" /></small>
                </Button>
              </div>
            </Col>
          </Row>
        </div>
        <TemplateRenderer options={config} showTooltips={showTooltips} {...props} setOptions={setConfig} />
      </div>
    </div>
  )
};

export default Webpage;

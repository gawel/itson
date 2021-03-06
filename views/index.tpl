% rebase('base.tpl', title=title, itson=itson)
<div class="back index text-center">
%if itson:
    <div class="alert alert-success">{{ title }}</div>
    % for r in sessions:
        <div>
        % if r['ended']:
            I surfed {{ r['size'] }}m waves during {{ r['duration'] }}
            % if r['report_url']:
              <a target="new" href="{{ r['report_url'] }}">@{{ r['spot'] }}</a>
            % else:
              @{{ r['spot'] }}
            % end
            % if r['comment']:
              <div>It was {{ r['comment'] }}</div>
            % end
        % else:
            I'm surfing
            % if r['report_url']:
              <a target="new" href="{{ r['report_url'] }}">@{{ r['spot'] }}</a>
            % else:
              @{{ r['spot'] }}
            % end
            since {{ r['duration'] }}.
        % end
        </div>
    %end
    </div>
%else:
    <div class="off">{{ title }}</div>
%end
</div>

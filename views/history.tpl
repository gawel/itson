% rebase('base.tpl', title=title, itson=itson)
<div class="row back">
    <table class="table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Spot</th>
                <th class="no-mobile">Started</th>
                <th class="no-mobile">Ended</th>
                <th>Duration</th>
                <th>Waves</th>
                <th class="no-mobile">Comment</th>
            </tr>
        </thead>
        <tbody>
        % for r in sessions:
            <tr id="{{ r.id }}">
              <td><a href="/sessions/{{ r.date.replace('-', '/') }}"
                     >{{r.date}}</a></td>
              <td>
                  % if r.report_url:
                    <a target="new" href="{{ r.report_url }}">@{{ r.spot }}</a>
                  % else:
                    @{{ r.spot }}
                  % end
              </td>
              <td class="no-mobile">{{r.started}}</td>
              <td class="no-mobile">{{r.ended or "Its ON!"}}</td>
              <td>{{r.duration or "Its ON!"}}</td>
              <td>{{r.size}}m</td>
              <td class="no-mobile">{{r.comment or ""}}</td>
            </tr>
        % end
        </tbody>
        <tfoot>
          <tr>
            <th>{{ total.date }} sessions</th>
            <th>{{ total.spot }} spots</th>
            <th class="no-mobile">&nbsp;</th>
            <th class="no-mobile">&nbsp;</th>
            <th>{{ total.duration }}</th>
            <th>{{ total.size }}m</th>
            <th class="no-mobile">&nbsp;</th>
          </tr>
        </tfoot>
    </table>
</div>
